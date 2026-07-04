# Problem Statement — Fahamika

## Background
Kenya's Persons with Disabilities Act guarantees a comprehensive set of rights: equality before the law, legal and financial capacity, marriage and family rights, privacy protections, and specific safeguards for women with disabilities (Sections 6–10). These are not abstract principles — they are enforceable legal rights governing property ownership, access to credit, reproductive autonomy, and protection from discrimination.

However, the gap between a right that exists on paper and a citizen who can actually exercise it is wide. Official civic content exists as dense, technical English PDFs published on government websites. Accessing them requires a smartphone or desktop computer, stable internet, and high English literacy. For a deaf smallholder in Homa Bay or a blind elder in Kilifi, these documents might as well not exist.

## The Problem
Persons with disabilities in Kenya cannot independently access information about their own legal rights. The information exists in government archives — but the last-mile delivery mechanism does not:

- **Format barrier:** PDFs in formal legal English, often 100+ pages
- **Device barrier:** Requires a smartphone or computer — inaccessible to citizens with only a feature phone
- **Connectivity barrier:** Requires stable internet — unrealistic in rural and peri-urban areas
- **Literacy barrier:** Written English only — excludes Swahili, Sheng, and vernacular-language speakers
- **Disability-specific barrier:** Visually impaired users cannot read the documents; hearing-impaired users have no sign-language alternative

## Target User
A person with a disability living in a rural or peri-urban area of Kenya. They may own a basic feature phone (not a smartphone), are comfortable with voice calls but not email or web browsing, and speak Swahili or a vernacular language rather than English. They currently learn about their rights through word-of-mouth, local radio, or community gatherings — channels that are unverifiable, inconsistent, and often incomplete.

## Current Alternatives & Their Shortcomings

| Channel | Shortcoming |
|---------|-------------|
| NGO hotlines | Staffed manually, limited hours, human-dependent — does not scale |
| Government websites | PDFs, English-only, requires smartphone + internet |
| Community barazas (meetings) | Infrequent, one-to-many, no way to revisit or verify information |
| Radio programs | Scheduled, not on-demand; cannot answer a specific question a caller has right now |
| SMS-based services | Text-only; inaccessible to blind users and low-literacy populations |
| Smartphone apps | Excludes the very population the service targets — feature-phone-only users |

None of these offer an on-demand, voice-first channel that works from any phone, in the caller's language, with factual accuracy guaranteed.

## Our Approach
A toll-free IVR phone service accessible from any feature phone — no smartphone, no internet, no literacy required. A citizen dials a number, hears a menu, and the system reads simplified civic information aloud in their language.

The system uses pre-approved civic content fetched from a Firestore database. An AI model (Ollama, running locally) simplifies the language to plain, accessible speech but is never permitted to invent facts — it only rewrites what already exists in the database. Text-to-speech is handled by Piper (neural TTS), and a planned speech-to-text extension (Whisper) will allow callers to ask questions aloud rather than navigate menus.

The design is deliberately local-first: the entire pipeline runs offline on a single Ubuntu server with a bridged softphone for testing. No per-call API costs, no dependency on cloud connectivity at call time. A cloud-based AI (Claude API) is evaluated as a fallback for higher-quality output where connectivity permits, but the default path works without the internet.

## Impact Hypothesis
When the barrier to accessing civic information drops from "own a smartphone, read English, and navigate a government PDF" to "dial a number and listen in Swahili," the accountability loop between citizen and government shortens. A citizen who knows their rights can demand them — from a landlord, a bank, a clinic, an employer. Closing this information gap restores a basic democratic mechanism: informed citizens ask better questions, make better decisions, and hold institutions accountable. For PWDs specifically, this is not an abstract improvement — it is the difference between a legal protection that exists and one that is actually usable.
