import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import yaml from 'js-yaml';
import {
  PRODUCT_STATUSES,
  type ProductCapability,
  type ProductDomain,
  type ProductEvidence,
  type ProductFeature,
  type ProductInstrumentData,
  type ProductStatus,
  type ProductStatusCounts,
  type ProductSummary,
} from '@/lib/product-model';

interface RawPostureEntity {
  readonly id?: unknown;
  readonly name?: unknown;
  readonly description?: unknown;
  readonly status?: unknown;
  readonly capability_ids?: unknown;
  readonly feature_ids?: unknown;
  readonly domain_id?: unknown;
  readonly capability_id?: unknown;
  readonly evidence?: unknown;
}

interface RawFeatureCatalogFeature {
  readonly id?: unknown;
  readonly name?: unknown;
  readonly status?: unknown;
  readonly notes?: unknown;
  readonly evidence?: unknown;
}

interface RawFeatureCatalogCapability {
  readonly slug?: unknown;
  readonly status?: unknown;
  readonly rollup_notes?: unknown;
  readonly features?: unknown;
}

interface RawFeatureCatalogDomain {
  readonly slug?: unknown;
  readonly status?: unknown;
  readonly rollup_notes?: unknown;
  readonly capabilities?: unknown;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function asString(value: unknown, fallback = ''): string {
  return typeof value === 'string' ? value : fallback;
}

function asArray<T>(value: unknown): T[] {
  return Array.isArray(value) ? (value as T[]) : [];
}

function normalizeStatus(raw: unknown): ProductStatus {
  if (PRODUCT_STATUSES.includes(raw as ProductStatus)) return raw as ProductStatus;
  const normalized = asString(raw).trim().toLowerCase();
  switch (normalized) {
    case 'released':
    case 'live':
    case 'applied':
      return 'live';
    case 'rollout':
    case 'partial':
      return 'partial';
    case 'development':
      return 'pilot';
    case 'cleanup':
      return 'dormant';
    case 'applied-and-evolving':
    case 'evolving':
      return 'partial';
    default:
      return 'planned';
  }
}

function normalizeEvidence(raw: unknown): ProductEvidence[] {
  return asArray<unknown>(raw)
    .map((entry) => {
      if (!isRecord(entry)) return null;
      const kind = entry.kind;
      if (
        kind !== 'artifact-defined' &&
        kind !== 'manually-curated' &&
        kind !== 'signal-supported'
      ) {
        return null;
      }
      const label = asString(entry.label).trim();
      if (!label) return null;
      return {
        kind,
        label,
        ...(asString(entry.detail).trim() ? { detail: asString(entry.detail).trim() } : {}),
      } satisfies ProductEvidence;
    })
    .filter((entry): entry is ProductEvidence => entry !== null);
}

function readMarkdownArtifact(filePath: string): { frontmatter: Record<string, unknown>; body: string } | null {
  try {
    if (!fs.existsSync(filePath)) return null;
    const raw = fs.readFileSync(filePath, 'utf-8');
    const parsed = matter(raw);
    return {
      frontmatter: isRecord(parsed.data) ? parsed.data : {},
      body: parsed.content.trim(),
    };
  } catch {
    return null;
  }
}

function readYamlFile(filePath: string): Record<string, unknown> | null {
  try {
    if (!fs.existsSync(filePath)) return null;
    const raw = fs.readFileSync(filePath, 'utf-8');
    const parsed = yaml.load(resolveGitConflictBlocks(raw), { json: true });
    return isRecord(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

function resolveGitConflictBlocks(raw: string): string {
  const lines = raw.split(/\r?\n/);
  const resolved: string[] = [];
  let mode: 'normal' | 'ours' | 'theirs' = 'normal';

  for (const line of lines) {
    if (line.startsWith('<<<<<<< ')) {
      mode = 'ours';
      continue;
    }
    if (line.startsWith('=======') && mode === 'ours') {
      mode = 'theirs';
      continue;
    }
    if (line.startsWith('>>>>>>> ') && mode !== 'normal') {
      mode = 'normal';
      continue;
    }
    if (mode === 'ours') continue;
    resolved.push(line);
  }

  return resolved.join('\n');
}

function humanizeSlug(slug: string): string {
  return slug
    .split('-')
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function pushArtifactEvidence(filePath: string, repoRoot: string): ProductEvidence[] {
  return fs.existsSync(filePath)
    ? [
        {
          kind: 'artifact-defined',
          label: path.relative(repoRoot, filePath),
        },
      ]
    : [];
}

function firstParagraph(markdown: string): string {
  return markdown
    .split(/\r?\n\r?\n/)
    .map((chunk) => chunk.replace(/^#+\s+/gm, '').trim())
    .find((chunk) => chunk.length > 40 && !chunk.startsWith('**Status:**'))
    ?.replace(/\s+/g, ' ')
    .slice(0, 240) ?? '';
}

function emptyStatusCounts(): ProductStatusCounts {
  return {
    live: 0,
    partial: 0,
    pilot: 0,
    planned: 0,
    dormant: 0,
  };
}

function tallyStatuses(statuses: ReadonlyArray<ProductStatus>): ProductStatusCounts {
  const counts: Record<ProductStatus, number> = {
    live: 0,
    partial: 0,
    pilot: 0,
    planned: 0,
    dormant: 0,
  };
  for (const status of statuses) counts[status] += 1;
  return counts;
}

function deriveCatalogHierarchy(
  repoRoot: string,
  productBasePath: string,
): {
  domains: ProductDomain[];
  capabilities: ProductCapability[];
  features: ProductFeature[];
  sourceArtifacts: string[];
  coverageGaps: string[];
} {
  const catalogPath = path.join(productBasePath, 'scope', 'features.yaml');
  const catalog = readYamlFile(catalogPath);
  if (!catalog) {
    return { domains: [], capabilities: [], features: [], sourceArtifacts: [], coverageGaps: [] };
  }

  const rawDomains = asArray<unknown>(catalog.domains);
  const features: ProductFeature[] = [];
  const capabilities: ProductCapability[] = [];
  const domains: ProductDomain[] = [];

  for (const domainEntry of rawDomains) {
    if (!isRecord(domainEntry)) continue;
    const rawDomain = domainEntry as RawFeatureCatalogDomain;
    const domainId = asString(rawDomain.slug).trim();
    if (!domainId) continue;

    const domainCapabilities: ProductCapability[] = [];
    for (const capabilityEntry of asArray<unknown>(rawDomain.capabilities)) {
      if (!isRecord(capabilityEntry)) continue;
      const rawCapability = capabilityEntry as RawFeatureCatalogCapability;
      const capabilityId = asString(rawCapability.slug).trim();
      if (!capabilityId) continue;

      const capabilityFeatures: ProductFeature[] = [];
      for (const featureEntry of asArray<unknown>(rawCapability.features)) {
        if (!isRecord(featureEntry)) continue;
        const rawFeature = featureEntry as RawFeatureCatalogFeature;
        const featureId = asString(rawFeature.id).trim();
        const featureName = asString(rawFeature.name).trim();
        if (!featureId || !featureName) continue;
        const feature: ProductFeature = {
          id: featureId,
          name: featureName,
          capabilityId,
          description: asString(rawFeature.notes).trim(),
          status: normalizeStatus(rawFeature.status),
          evidence: pushArtifactEvidence(catalogPath, repoRoot),
        };
        capabilityFeatures.push(feature);
        features.push(feature);
      }

      const capability: ProductCapability = {
        id: capabilityId,
        name: humanizeSlug(capabilityId),
        domainId,
        description: asString(rawCapability.rollup_notes).trim(),
        status: normalizeStatus(rawCapability.status),
        featureIds: capabilityFeatures.map((feature) => feature.id),
        evidence: pushArtifactEvidence(catalogPath, repoRoot),
        features: capabilityFeatures,
      };
      domainCapabilities.push(capability);
      capabilities.push(capability);
    }

    domains.push({
      id: domainId,
      name: humanizeSlug(domainId),
      description: asString(rawDomain.rollup_notes).trim(),
      status: normalizeStatus(rawDomain.status),
      capabilityIds: domainCapabilities.map((capability) => capability.id),
      evidence: pushArtifactEvidence(catalogPath, repoRoot),
      capabilities: domainCapabilities,
    });
  }

  const coverageGaps: string[] = [];
  if (domains.length === 0) {
    coverageGaps.push('Product catalog exists, but no domains could be derived from scope/features.yaml.');
  }

  return {
    domains,
    capabilities,
    features,
    sourceArtifacts: fs.existsSync(catalogPath) ? [path.relative(repoRoot, catalogPath)] : [],
    coverageGaps,
  };
}

export function loadProductInstrumentData(repoRoot: string, productBasePath: string): ProductInstrumentData {
  const posturePath = path.join(productBasePath, 'posture.yaml');
  const visionPath = path.join(productBasePath, 'vision.md');
  const roadmapPath = path.join(productBasePath, 'roadmap.md');
  const engineeringPath = path.join(productBasePath, 'roadmap-engineering.md');

  const rawPosture = readYamlFile(posturePath) ?? {};
  const vision = readMarkdownArtifact(visionPath);

  const productBlock = isRecord(rawPosture.product) ? rawPosture.product : {};
  const sourceArtifacts = [visionPath, roadmapPath, engineeringPath, posturePath]
    .filter((filePath) => fs.existsSync(filePath))
    .map((filePath) => path.relative(repoRoot, filePath));

  const summary: ProductSummary = {
    name:
      asString(productBlock.name).trim() ||
      asString(vision?.frontmatter.product).trim() ||
      asString(vision?.frontmatter.title).trim() ||
      'Untitled Product',
    slug:
      asString(productBlock.slug).trim() ||
      asString(vision?.frontmatter.slug).trim() ||
      'product',
    headline:
      asString(productBlock.headline).trim() ||
      'Fused product posture from curated artifacts, ready for future signal enrichment.',
    description:
      asString(productBlock.description).trim() ||
      firstParagraph(vision?.body ?? '') ||
      'No product summary is available yet. Add `.garura/product/posture.yaml` and supporting product artifacts to enrich this surface.',
    sourceArtifacts,
  };

  const features: ProductFeature[] = [];
  for (const entry of asArray<unknown>(rawPosture.features)) {
    if (!isRecord(entry)) continue;
    const rawFeature = entry as RawPostureEntity;
    const id = asString(rawFeature.id).trim();
    const name = asString(rawFeature.name).trim();
    const capabilityId = asString(rawFeature.capability_id).trim();
    if (!id || !name || !capabilityId) continue;
    features.push({
      id,
      name,
      capabilityId,
      description: asString(rawFeature.description).trim(),
      status: normalizeStatus(rawFeature.status),
      evidence: normalizeEvidence(rawFeature.evidence),
    });
  }

  const featuresByCapability = new Map<string, ProductFeature[]>();
  for (const feature of features) {
    const list = featuresByCapability.get(feature.capabilityId) ?? [];
    list.push(feature);
    featuresByCapability.set(feature.capabilityId, list);
  }

  const capabilities: ProductCapability[] = [];
  for (const entry of asArray<unknown>(rawPosture.capabilities)) {
    if (!isRecord(entry)) continue;
    const rawCapability = entry as RawPostureEntity;
    const id = asString(rawCapability.id).trim();
    const name = asString(rawCapability.name).trim();
    const domainId = asString(rawCapability.domain_id).trim();
    if (!id || !name || !domainId) continue;
    const resolvedFeatures = featuresByCapability.get(id) ?? [];
    const declaredFeatureIds = asArray<string>(rawCapability.feature_ids)
      .map((value) => asString(value).trim())
      .filter(Boolean);
    capabilities.push({
      id,
      name,
      domainId,
      description: asString(rawCapability.description).trim(),
      status: normalizeStatus(rawCapability.status),
      featureIds:
        declaredFeatureIds.length > 0
          ? declaredFeatureIds
          : resolvedFeatures.map((feature) => feature.id),
      evidence: normalizeEvidence(rawCapability.evidence),
      features: resolvedFeatures,
    });
  }

  const capabilitiesByDomain = new Map<string, ProductCapability[]>();
  for (const capability of capabilities) {
    const list = capabilitiesByDomain.get(capability.domainId) ?? [];
    list.push(capability);
    capabilitiesByDomain.set(capability.domainId, list);
  }

  const domains: ProductDomain[] = [];
  for (const entry of asArray<unknown>(rawPosture.domains)) {
    if (!isRecord(entry)) continue;
    const rawDomain = entry as RawPostureEntity;
    const id = asString(rawDomain.id).trim();
    const name = asString(rawDomain.name).trim();
    if (!id || !name) continue;
    const resolvedCapabilities = capabilitiesByDomain.get(id) ?? [];
    const declaredCapabilityIds = asArray<string>(rawDomain.capability_ids)
      .map((value) => asString(value).trim())
      .filter(Boolean);
    domains.push({
      id,
      name,
      description: asString(rawDomain.description).trim(),
      status: normalizeStatus(rawDomain.status),
      capabilityIds:
        declaredCapabilityIds.length > 0
          ? declaredCapabilityIds
          : resolvedCapabilities.map((capability) => capability.id),
      evidence: normalizeEvidence(rawDomain.evidence),
      capabilities: resolvedCapabilities,
    });
  }

  const derivedCatalog = domains.length === 0 ? deriveCatalogHierarchy(repoRoot, productBasePath) : null;
  const resolvedDomains = derivedCatalog ? derivedCatalog.domains : domains;
  const resolvedCapabilities = derivedCatalog ? derivedCatalog.capabilities : capabilities;
  const resolvedFeatures = derivedCatalog ? derivedCatalog.features : features;

  const allStatuses: ProductStatus[] = [
    ...resolvedDomains.map((entry) => entry.status),
    ...resolvedCapabilities.map((entry) => entry.status),
    ...resolvedFeatures.map((entry) => entry.status),
  ];
  const coverageGaps: string[] = [];

  if (resolvedDomains.length === 0) coverageGaps.push('No curated domains are defined in posture.yaml yet.');
  if (resolvedCapabilities.some((entry) => !resolvedDomains.some((domain) => domain.id === entry.domainId))) {
    coverageGaps.push('One or more capabilities reference a missing domain.');
  }
  if (resolvedFeatures.some((entry) => !resolvedCapabilities.some((capability) => capability.id === entry.capabilityId))) {
    coverageGaps.push('One or more features reference a missing capability.');
  }
  if (resolvedDomains.some((entry) => entry.capabilities.length === 0)) {
    coverageGaps.push('At least one domain has no mapped capabilities yet.');
  }
  if (resolvedCapabilities.some((entry) => entry.features.length === 0)) {
    coverageGaps.push('At least one capability has no mapped features yet.');
  }

  if (derivedCatalog) {
    coverageGaps.push(
      ...derivedCatalog.coverageGaps,
      'Rendering from scope/features.yaml because posture.yaml is not present.',
    );
  }

  const evidence = [...resolvedDomains, ...resolvedCapabilities, ...resolvedFeatures].flatMap(
    (entry) => entry.evidence,
  );
  const updatedAt = asString(rawPosture.updated_at).trim() || asString(vision?.frontmatter.last_updated).trim() || null;

  const resolvedSummary: ProductSummary = {
    ...summary,
    sourceArtifacts: Array.from(
      new Set([...summary.sourceArtifacts, ...(derivedCatalog?.sourceArtifacts ?? [])]),
    ),
    description:
      summary.description.startsWith('No product summary is available yet.') && derivedCatalog
        ? 'Derived from the existing product feature catalog while curated posture metadata is absent.'
        : summary.description,
  };

  return {
    summary: resolvedSummary,
    updatedAt,
    statusCounts: tallyStatuses(allStatuses),
    domains: resolvedDomains,
    coverageGaps,
    signalsSummary: {
      artifactDefined: evidence.filter((entry) => entry.kind === 'artifact-defined').length,
      manuallyCurated: evidence.filter((entry) => entry.kind === 'manually-curated').length,
      signalSupported: evidence.filter((entry) => entry.kind === 'signal-supported').length,
      runtimeSignalsConnected: false,
      note: 'Runtime product signals are not wired yet. This surface is shaped to absorb OTEL and usage evidence later.',
    },
  };
}
