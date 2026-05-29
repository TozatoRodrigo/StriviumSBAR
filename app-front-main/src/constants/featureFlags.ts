export const isExperimentalSbarVoiceDictationEnabled = () =>
  process.env.NEXT_PUBLIC_EXPERIMENTAL_SBAR_VOICE_DICTATION === 'true'

export const isExperimentalSbarAiDictationEnabled = () =>
  process.env.NEXT_PUBLIC_EXPERIMENTAL_SBAR_AI_DICTATION === 'true'
