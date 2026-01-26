import fs from "fs";
import path from "path";

type JobMeta = {
	description: string;
	filesChanged?: number;
	estimatedLOC?: number;
	declaredComplexity?: "low" | "medium" | "high";
};

type Policy = {
	maxInteractions: number;
	preferredMode: string;
	autoSummarize: boolean;
	suggestSplit: boolean;
};

const cfgPath = path.join(__dirname, "adaptive_limits.json");
const cfg = JSON.parse(fs.readFileSync(cfgPath, "utf8"));

function classifyJob(meta: JobMeta): "small" | "medium" | "large" {
	const descLen = (meta.description || "").length;
	const files = meta.filesChanged ?? 0;
	const loc = meta.estimatedLOC ?? 0;
	const complexityScore =
		(meta.declaredComplexity === "high" ? 1.5 : meta.declaredComplexity === "medium" ? 1.0 : 0.5);

	// Simple scoring heuristic
	const score =
		descLen / 1000 + files * 0.3 + loc / 1000 * complexityScore;

	if (descLen <= cfg.thresholds.small.desc_length && files <= cfg.thresholds.small.files_changed && loc <= cfg.thresholds.small.estimated_loc) {
		return "small";
	}
	if (descLen <= cfg.thresholds.medium.desc_length && files <= cfg.thresholds.medium.files_changed && loc <= cfg.thresholds.medium.estimated_loc) {
		return "medium";
	}
	return "large";
}

export function getPolicyForJob(meta: JobMeta): Policy {
	const size = classifyJob(meta);
	return cfg.policies[size];
}

/** Compact summarizer: keep first N chars and extract key bullets (placeholder) */
export function quickSummarize(text: string, maxChars = 400): string {
	if (!text) return "";
	if (text.length <= maxChars) return text;
	// naive summarization: keep head + tail to preserve context
	const head = text.slice(0, Math.floor(maxChars * 0.6));
	const tail = text.slice(-Math.floor(maxChars * 0.4));
	return `${head.trim()} … ${tail.trim()}`;
}
