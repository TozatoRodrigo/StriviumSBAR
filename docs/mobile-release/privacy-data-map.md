# Privacy and Data Safety Map

This document is the source checklist for Apple App Privacy and Google Play Data safety declarations. Legal review should approve the final store answers before submission.

## Data Categories Used by the App

| Data | Examples | Purpose | Linked to user | Shared externally |
| --- | --- | --- | --- | --- |
| Account data | Name, email, phone, CRM, document | Authentication, user profile, authorization | Yes | No, except infrastructure processors |
| Workspace data | Organization/workspace membership, roles | Tenant access control | Yes | No, except infrastructure processors |
| Patient data | Name, document, birth date, hospitalization details | Clinical operations workflow | Yes | No, except infrastructure processors |
| Clinical notes | Evolutions, hospitalization actions, attachments | Care-team documentation workflow | Yes | No, except infrastructure processors |
| Authentication data | Access tokens, refresh tokens | Sign-in and session continuity | Yes | No |
| Device/network data | Timezone, IP visible to backend logs | Security, audit, localization | May be linked | Infrastructure processors |
| Anti-abuse data | Cloudflare Turnstile token | Bot protection for sign-in/sign-up | May be linked | Cloudflare |

## First Release Feature Flags

- `NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION=false`
- `NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION=false`

If either feature is enabled later, update store privacy answers, in-app disclosures, permission strings, review notes, screenshots, and medical review wording before submission.

## Required Disclosures

- The privacy policy must describe collection, use, retention, deletion, support contact, processors, and security practices.
- Google Play Health apps declaration must be completed because the app handles health-related workflows and sensitive health data.
- Apple App Privacy must disclose collected data types and whether data is linked to the user.
- If regulated medical-device claims are made later, submit the appropriate regulatory documentation or remove the claim.

## Security Controls Expected Before Production

- HTTPS only for web and API.
- No localhost or private API hosts in store builds.
- S3 or equivalent production object storage for attachments.
- Production SMTP with TLS.
- Strong JWT secret unique per environment.
- Database backups and restore procedure.
- Access logs and error monitoring.
