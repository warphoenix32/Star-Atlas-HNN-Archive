# Star Atlas Transcription Standard

## Purpose

This standard governs future machine-assisted transcription of Star Atlas
audio and video. It applies during `PRESERVE`; later semantic evaluation still
uses the [Evidence Significance Standard](EVIDENCE-SIGNIFICANCE-STANDARD.md).

The objective is a complete, timestamped research record with explicit
uncertainty. Speaker identification is useful when evidenced, but it is not a
precondition for preserving information-centered discussion.

The machine-readable defaults are in
[`star-atlas-transcription-profile.json`](star-atlas-transcription-profile.json).

## Required evidence layers

Every transcription campaign must keep these layers distinct:

1. **Source capture record** — source URL or supplied artifact, source checksum,
   capture method, capture time, media duration, and available native captions.
2. **Raw ASR output** — immutable model output with segment and word timestamps,
   model identity, model revision or fingerprint, inference settings, hardware,
   and quality signals.
3. **Normalized transcript** — a derived human-readable transcript. Spelling,
   punctuation, and terminology corrections are allowed only when logged.
4. **Correction ledger** — original text, corrected text, timestamp, reason,
   confidence, and reviewer or deterministic rule.
5. **Review queue** — uncertain terminology, low-confidence spans, repetition,
   timestamp anomalies, and attribution-dependent statements.

Never silently replace raw ASR output with corrected text.

## Performance profiles

### CPU archival baseline

- Model: `small.en`
- Device: `cpu`
- Compute type: `int8`
- Threads: begin with physical CPU cores minus two, with a floor of four
- Workers: one for a single recording
- Language: explicitly `en`
- Beam size: five
- Temperature: zero
- Word timestamps: enabled
- Voice activity detection: enabled, initially using 1,000 ms minimum silence

Record the resolved thread count. Benchmark representative five-minute audio at
several thread counts when the hardware is new; the fastest stable setting
becomes campaign-local, not a universal hardware claim.

### GPU archival-quality profile

- Model: `large-v3-turbo`
- Device: `cuda`
- Compute type: `float16`; use `int8_float16` when memory requires it
- Language: explicitly `en`
- Beam size: five
- Temperature: zero
- Word timestamps: enabled
- Voice activity detection: enabled with the same initial silence policy

Record CUDA, cuDNN, GPU, driver, package, model, and compute-type versions.

## Two-pass quality policy

The first pass produces full recording coverage. A stronger or focused second
pass is required for spans showing one or more of:

- low average log probability;
- high compression or repeated text;
- suspicious no-speech behavior;
- malformed Star Atlas terminology or named entities;
- discontinuous or implausible timestamps;
- disagreement with adjacent context or native captions;
- a potentially important claim whose wording remains uncertain.

Second-pass work may use the GPU quality profile or timestamp-bounded
retranscription. Preserve both readings when they materially disagree. Model
agreement raises recognition confidence; it does not prove the factual claim.

## Vocabulary assistance

Use the controlled hotword list in the machine-readable profile. Hotwords and
initial prompts are recognition aids, not evidence. They may include verified
Star Atlas names and terms, but must not contain proposed facts, quotations, or
speculative identity resolutions.

## Speaker policy

Do not infer a speaker from topic, vocabulary, voice similarity, speaking order,
or the candidate roster alone.

For Atlas Brew, the operator-supplied recurring-speaker candidates are:

- Jose;
- Dominic;
- Santi;
- Michael Wagner, who often appears as a guest.

These names may improve recognition of spoken names and may be shown to a human
reviewer. They must remain `UNASSIGNED_CANDIDATE` until the recording, visible
label, introduction, reliable show metadata, or human adjudication supports a
specific segment attribution.

Each segment retains:

- `speaker_attribution`: observed name or `UNKNOWN`;
- `speaker_attribution_basis`;
- `speaker_dependency`: `NONE`, `PARTIAL`, or `REQUIRED`;
- `manual_speaker_review_required`.

Unknown speakers do not reduce recognition confidence automatically. They block
named quotations and person-specific institutional claims when speaker
dependency is `REQUIRED`.

## Archival acceptance

A transcript is acceptable only when:

- source and ASR checksums reconcile;
- the full media duration is accounted for or gaps are enumerated;
- every segment and word timestamp is within the media duration;
- raw and normalized artifacts remain distinguishable;
- all corrections are ledgered;
- package, model, settings, and hardware are recorded;
- native captions, when present, are preserved separately;
- low-confidence and attribution-dependent spans remain visible;
- no speaker is assigned solely from the Atlas Brew candidate roster;
- validation reports the profile used and every deviation.
