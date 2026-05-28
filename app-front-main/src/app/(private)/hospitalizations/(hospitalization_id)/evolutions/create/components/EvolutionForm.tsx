'use client'

import {
  Alert,
  Box,
  Checkbox,
  Chip,
  FormControlLabel,
  FormHelperText,
  InputAdornment,
  LinearProgress,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from '@mui/material'
import AssignmentTurnedInOutlinedIcon from '@mui/icons-material/AssignmentTurnedInOutlined'
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh'
import FactCheckOutlinedIcon from '@mui/icons-material/FactCheckOutlined'
import ShieldOutlinedIcon from '@mui/icons-material/ShieldOutlined'
import { useMemo, useState, type ReactNode } from 'react'
import { ImagesPreview } from './ImagesPreview'
import { InputImage } from './InputImage'
import { Controller, useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import {
  clinicalCourseOptions,
  defaultEvolutionType,
  priorityOptions,
  typeOptions,
} from '@/constants/evolutions'
import { EvolutionFormData, EvolutionSchema } from '@/validations/evolution'
import { EvolutionSbar, Media } from '@/hooks/queries/evolutions'
import { useResetOnDataChange } from '@/hooks/useResetOnDataChange'
import {
  isExperimentalSbarAiDictationEnabled,
  isExperimentalSbarVoiceDictationEnabled,
} from '@/constants/featureFlags'
import { VoiceDictationButton } from '@/components/VoiceDictationButton'
import type { SbarConfidence, SbarExtractResponse } from '@/hooks/mutations/sbar'
import { SbarDictationPanel } from './SbarDictationPanel'

type EvolutionFormInitialData = Partial<EvolutionFormData> & {
  description?: string
  medias?: Media[]
  sbar?: EvolutionSbar | null
}

type EvolutionFormProps = {
  allowOutcomeSelection?: boolean
  formId?: string
  hospitalizationId?: string
  initialData?: EvolutionFormInitialData
  submitAction: (payload: FormData) => void
  isPending: boolean
}

type SbarVoiceFieldName =
  | 'situation'
  | 'background'
  | 'assessment'
  | 'recommendation'
  | 'plan'
  | 'pending_items'
  | 'alerts'

type SbarAiFieldName = 'situation' | 'background' | 'assessment' | 'recommendation' | 'plan'

type AiDraftState = {
  confidence: SbarConfidence
  generated: boolean
  missingInformation: string[]
  reviewConfirmed: boolean
  sourceTranscript: string
  warnings: string[]
}

const id = 'evolution-form'

const normalizeInitialData = (initialData?: EvolutionFormInitialData): EvolutionFormData => ({
  type: initialData?.type ?? defaultEvolutionType,
  situation: initialData?.situation ?? initialData?.sbar?.situation ?? initialData?.description ?? '',
  background: initialData?.background ?? initialData?.sbar?.background ?? '',
  assessment: initialData?.assessment ?? initialData?.sbar?.assessment ?? '',
  recommendation: initialData?.recommendation ?? initialData?.sbar?.recommendation ?? '',
  plan: initialData?.plan ?? initialData?.sbar?.plan ?? '',
  priority: initialData?.priority ?? initialData?.sbar?.priority ?? 'routine',
  clinical_course: initialData?.clinical_course ?? initialData?.sbar?.clinical_course ?? '',
  pending_items: initialData?.pending_items ?? initialData?.sbar?.pending_items ?? '',
  alerts: initialData?.alerts ?? initialData?.sbar?.alerts ?? '',
  medias: initialData?.medias,
})

const appendIfFilled = (formData: FormData, key: string, value?: string | null) => {
  const trimmedValue = value?.trim()
  if (trimmedValue) {
    formData.append(key, trimmedValue)
  }
}

const buildSbarDescription = (data: EvolutionFormData) =>
  [
    `Situação: ${data.situation.trim()}`,
    data.background?.trim() ? `Contexto: ${data.background.trim()}` : null,
    `Avaliação: ${data.assessment.trim()}`,
    `Recomendação: ${data.recommendation.trim()}`,
    data.plan?.trim() ? `Plano: ${data.plan.trim()}` : null,
    data.pending_items?.trim() ? `Pendências: ${data.pending_items.trim()}` : null,
    data.alerts?.trim() ? `Alertas: ${data.alerts.trim()}` : null,
  ]
    .filter(Boolean)
    .join('\n')

const priorityColor = {
  routine: 'success',
  attention: 'warning',
  critical: 'error',
} as const

type SectionProps = {
  accent?: 'primary' | 'info' | 'success' | 'warning' | 'error'
  aiGenerated?: boolean
  children: ReactNode
  complete?: boolean
  letter: string
  subtitle: string
  title: string
}

const Section = ({
  accent = 'primary',
  aiGenerated = false,
  children,
  complete = false,
  letter,
  subtitle,
  title,
}: SectionProps) => (
  <Box
    sx={{
      border: theme => `1px solid ${theme.palette.divider}`,
      borderRadius: 2,
      bgcolor: 'background.paper',
      overflow: 'hidden',
    }}
  >
    <Stack direction="row" alignItems="stretch">
      <Box sx={{ width: 5, bgcolor: `${accent}.main`, flexShrink: 0 }} />
      <Box sx={{ flex: 1, minWidth: 0, p: { xs: 2, sm: 2.5 } }}>
        <Stack direction="row" justifyContent="space-between" gap={1.5} alignItems="flex-start" sx={{ mb: 2 }}>
          <Stack direction="row" gap={1.25} alignItems="flex-start" sx={{ minWidth: 0 }}>
            <Box
              sx={{
                alignItems: 'center',
                bgcolor: `${accent}.main`,
                borderRadius: 1.25,
                color: `${accent}.contrastText`,
                display: 'flex',
                flexShrink: 0,
                fontSize: 14,
                fontWeight: 900,
                height: 34,
                justifyContent: 'center',
                width: 34,
              }}
            >
              {letter}
            </Box>
            <Box sx={{ minWidth: 0 }}>
              <Typography fontWeight={800} color="text.primary">
                {title}
              </Typography>
              <Typography fontSize={13} color="text.secondary">
                {subtitle}
              </Typography>
            </Box>
          </Stack>
          <Stack direction="row" gap={0.75} flexWrap="wrap" justifyContent="flex-end">
            {aiGenerated && <Chip label="Rascunho IA" size="small" color="warning" variant="outlined" />}
            <Chip label={complete ? 'Preenchido' : 'Pendente'} size="small" color={complete ? 'success' : 'default'} variant={complete ? 'filled' : 'outlined'} />
          </Stack>
        </Stack>
        <Stack gap={2}>{children}</Stack>
      </Box>
    </Stack>
  </Box>
)

const confidencePercent = (value?: number) => {
  const normalized = Math.max(0, Math.min(100, Math.round((value ?? 0) * 100)))
  return `${normalized}%`
}

const hasText = (value?: string | null) => Boolean(value?.trim())
const dischargeTypeId = 'hospitalization_discharge'
const deceasedTypeId = 'hospitalization_deceased'
const closingOutcomeTypeIds = new Set([dischargeTypeId, deceasedTypeId])

export const EvolutionForm = ({
  allowOutcomeSelection = true,
  formId = id,
  hospitalizationId,
  submitAction,
  isPending,
  initialData,
}: EvolutionFormProps) => {
  const normalizedInitialData = useMemo(() => normalizeInitialData(initialData), [initialData])
  const voiceDictationEnabled = isExperimentalSbarVoiceDictationEnabled()
  const aiDictationEnabled = isExperimentalSbarAiDictationEnabled()
  const [images, setImages] = useState<File[]>([])
  const [existingImages, setExistingImages] = useState<Media[]>(
    initialData?.medias?.filter(m => m.type === 'photo') ?? []
  )
  const [removedImages, setRemovedImages] = useState<string[]>([])
  const [aiDraft, setAiDraft] = useState<AiDraftState | null>(null)
  const [aiReviewError, setAiReviewError] = useState(false)

  const handleRemoveNew = (indexToRemove: number) => {
    setImages(prev => prev.filter((_, index) => index !== indexToRemove))
  }
  const handleRemoveExisting = (media: Media) => {
    setExistingImages(prev => prev.filter(m => m.id !== media.id))
    setRemovedImages(prev => [...prev, media.id])
  }

  const {
    register,
    handleSubmit,
    control,
    getValues,
    reset,
    setValue,
    watch,
    formState: { errors },
  } = useForm<EvolutionFormData>({
    resolver: zodResolver(EvolutionSchema),
    defaultValues: normalizedInitialData,
  })

  const watchedFields = watch()
  const requiredCompleted = [
    hasText(watchedFields.situation),
    hasText(watchedFields.assessment),
    hasText(watchedFields.recommendation),
  ].filter(Boolean).length
  const optionalCompleted = [
    hasText(watchedFields.background),
    hasText(watchedFields.plan),
    hasText(watchedFields.pending_items),
    hasText(watchedFields.alerts),
  ].filter(Boolean).length
  const completionPercent = Math.round(((requiredCompleted + optionalCompleted) / 7) * 100)
  const reviewReady = !aiDraft?.generated || aiDraft.reviewConfirmed
  const hasNoGroundedCoverage =
    !!aiDraft?.generated &&
    Object.values(aiDraft.confidence).every(confidenceValue => confidenceValue <= 0)
  const selectedOutcomeType = watchedFields.type ?? defaultEvolutionType
  const closesHospitalization =
    selectedOutcomeType === dischargeTypeId || selectedOutcomeType === deceasedTypeId

  const onSubmit = async (data: EvolutionFormData) => {
    if (aiDraft?.generated && !aiDraft.reviewConfirmed) {
      setAiReviewError(true)
      return
    }

    if (allowOutcomeSelection && closingOutcomeTypeIds.has(data.type)) {
      const userConfirmedClose = window.confirm(
        'Confirmar desfecho de alta/óbito? Essa ação encerra a internação atual e remove o paciente da lista de pendentes.'
      )
      if (!userConfirmedClose) {
        return
      }
    }

    const formData = new FormData()
    const description = buildSbarDescription(data)

    formData.append('description', description)
    formData.append('action_type', data.type)
    formData.append('sbar_situation', data.situation.trim())
    appendIfFilled(formData, 'sbar_background', data.background)
    formData.append('sbar_assessment', data.assessment.trim())
    formData.append('sbar_recommendation', data.recommendation.trim())
    appendIfFilled(formData, 'sbar_plan', data.plan)
    formData.append('sbar_priority', data.priority)
    appendIfFilled(formData, 'sbar_clinical_course', data.clinical_course)
    appendIfFilled(formData, 'sbar_pending_items', data.pending_items)
    appendIfFilled(formData, 'sbar_alerts', data.alerts)

    if (aiDraft?.generated) {
      formData.append('sbar_source_transcript', aiDraft.sourceTranscript)
      formData.append('sbar_ai_generated', String(aiDraft.generated))
      formData.append('sbar_ai_review_confirmed', String(aiDraft.reviewConfirmed))
      formData.append('sbar_ai_warnings', JSON.stringify(aiDraft.warnings))
      formData.append('sbar_ai_missing_information', JSON.stringify(aiDraft.missingInformation))
      formData.append('sbar_ai_confidence', JSON.stringify(aiDraft.confidence))
    }

    images.forEach(file => {
      formData.append('files', file)
    })

    if (removedImages.length) {
      removedImages.forEach((id, index) => {
        formData.append(`removed_images_ids[${index}]`, id)
      })
    }
    submitAction(formData)
  }

  const appendTranscriptToField = (fieldName: SbarVoiceFieldName, transcript: string) => {
    const currentValue = getValues(fieldName)?.trim()
    const transcriptValue = transcript.trim()
    const nextValue = currentValue ? `${currentValue} ${transcriptValue}` : transcriptValue

    setValue(fieldName, nextValue, {
      shouldDirty: true,
      shouldValidate: true,
    })
  }

  const applyAiDraft = (result: SbarExtractResponse, sourceTranscript: string) => {
    const fields: Array<[SbarAiFieldName, string]> = [
      ['situation', result.situation],
      ['background', result.background],
      ['assessment', result.assessment],
      ['recommendation', result.recommendation],
      ['plan', result.plan],
    ]

    fields.forEach(([fieldName, value]) => {
      setValue(fieldName, value, {
        shouldDirty: true,
        shouldValidate: true,
      })
    })

    setAiDraft({
      confidence: result.confidence,
      generated: true,
      missingInformation: result.missing_information,
      reviewConfirmed: false,
      sourceTranscript,
      warnings: result.warnings,
    })
    setAiReviewError(false)
  }

  const voiceAdornment = (fieldName: SbarVoiceFieldName, fieldLabel: string) => {
    if (!voiceDictationEnabled) return {}

    return {
      slotProps: {
        input: {
          endAdornment: (
            <InputAdornment position="end" sx={{ alignSelf: 'flex-start', mt: 1 }}>
              <VoiceDictationButton
                disabled={isPending}
                fieldLabel={fieldLabel}
                onTranscript={transcript => appendTranscriptToField(fieldName, transcript)}
              />
            </InputAdornment>
          ),
        },
      },
    }
  }

  useResetOnDataChange(normalizedInitialData, reset)

  return (
    <Stack
      id={formId}
      className="p-4"
      flex={1}
      gap={2}
      component="form"
      encType="multipart/form-data"
      onSubmit={handleSubmit(onSubmit)}
      sx={{ bgcolor: 'grey.50', overflowY: 'auto', pb: 3 }}
    >
      <Box sx={{ maxWidth: 1180, width: '100%', mx: 'auto' }}>
        <Stack gap={2.5}>
          <Box
            sx={{
              bgcolor: 'background.paper',
              border: theme => `1px solid ${theme.palette.divider}`,
              borderRadius: 2,
              p: { xs: 2, sm: 2.5 },
            }}
          >
            <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" gap={2}>
              <Box>
                <Typography fontSize={12} fontWeight={800} color="primary.main" sx={{ letterSpacing: 0.4, textTransform: 'uppercase' }}>
                  Visita hospitalar
                </Typography>
                <Typography fontSize={{ xs: 22, sm: 26 }} fontWeight={900} color="text.primary">
                  Registrar evolução em SBAR
                </Typography>
                <Typography fontSize={13} color="text.secondary" sx={{ mt: 0.5, maxWidth: 680 }}>
                  Dite livremente, revise o texto bruto e salve somente depois de confirmar o rascunho clínico.
                </Typography>
              </Box>
              <Stack direction="row" gap={1} flexWrap="wrap" alignItems="flex-start">
                <Chip icon={<AssignmentTurnedInOutlinedIcon />} label={`${completionPercent}% preenchido`} size="small" color={completionPercent >= 70 ? 'success' : 'default'} variant={completionPercent >= 70 ? 'filled' : 'outlined'} />
                <Chip icon={<FactCheckOutlinedIcon />} label={reviewReady ? 'Revisão ok' : 'Revisão pendente'} size="small" color={reviewReady ? 'success' : 'warning'} variant="outlined" />
                <Chip icon={<ShieldOutlinedIcon />} label="Texto bruto auditável" size="small" color="info" variant="outlined" />
              </Stack>
            </Stack>
            <LinearProgress
              value={completionPercent}
              variant="determinate"
              sx={{ borderRadius: 999, height: 7, mt: 2 }}
            />
            {voiceDictationEnabled && (
              <Typography fontSize={12} color="text.secondary" sx={{ mt: 1 }}>
                Ditado usa recurso do navegador; o Strivium não armazena áudio.
              </Typography>
            )}
            <Controller
              name="type"
              control={control}
              render={({ field }) => (
                <TextField
                  select
                  fullWidth
                  variant="filled"
                  label="Desfecho da internação"
                  {...field}
                  value={field.value ?? defaultEvolutionType}
                  disabled={isPending || !allowOutcomeSelection}
                  error={!!errors.type}
                  helperText={errors.type?.message}
                  sx={{ mt: 2 }}
                >
                  {typeOptions.map(option => (
                    <MenuItem key={option.id} value={option.id}>
                      {option.id === defaultEvolutionType && 'Manter internado (visita)'}
                      {option.id === dischargeTypeId && 'Alta hospitalar'}
                      {option.id === deceasedTypeId && 'Óbito'}
                    </MenuItem>
                  ))}
                </TextField>
              )}
            />
            {closesHospitalization && (
              <Alert severity="warning" sx={{ mt: 2 }}>
                Salvar essa evolução com desfecho de alta ou óbito encerra a internação atual e o paciente sai da lista de pendentes.
              </Alert>
            )}
          </Box>

          {aiDictationEnabled && (
            <SbarDictationPanel
              disabled={isPending}
              hospitalizationId={hospitalizationId}
              onApply={applyAiDraft}
            />
          )}

          {aiDraft?.generated && (
            <Alert
              icon={<AutoFixHighIcon fontSize="inherit" />}
              severity={aiReviewError ? 'error' : aiDraft.reviewConfirmed ? 'success' : 'warning'}
              sx={{
                '& .MuiAlert-message': { width: '100%' },
                border: theme => `1px solid ${aiReviewError ? theme.palette.error.light : theme.palette.warning.light}`,
              }}
            >
              <Stack gap={1.25}>
                <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" gap={1}>
                  <Box>
                    <Typography fontSize={14} fontWeight={800}>
                      Rascunho SBAR gerado automaticamente
                    </Typography>
                    <Typography fontSize={13}>
                      Compare os campos com o texto bruto e confirme a revisão médica antes de salvar.
                    </Typography>
                    <Typography fontSize={12} color="text.secondary" sx={{ mt: 0.5 }}>
                      Percentuais indicam cobertura factual do texto bruto em cada campo SBAR.
                    </Typography>
                  </Box>
                  <Stack direction="row" gap={0.75} flexWrap="wrap">
                    <Chip label={`S ${confidencePercent(aiDraft.confidence.situation)}`} size="small" />
                    <Chip label={`B ${confidencePercent(aiDraft.confidence.background)}`} size="small" />
                    <Chip label={`A ${confidencePercent(aiDraft.confidence.assessment)}`} size="small" />
                    <Chip label={`R ${confidencePercent(aiDraft.confidence.recommendation)}`} size="small" />
                    <Chip label={`P ${confidencePercent(aiDraft.confidence.plan)}`} size="small" />
                  </Stack>
                </Stack>
                {!!aiDraft.warnings.length && (
                  <Typography fontSize={13}>
                    Atenções: {aiDraft.warnings.join(' · ')}
                  </Typography>
                )}
                {!!aiDraft.missingInformation.length && (
                  <Typography fontSize={13}>
                    Ausentes/ambíguas: {aiDraft.missingInformation.join(' · ')}
                  </Typography>
                )}
                {hasNoGroundedCoverage && (
                  <Typography fontSize={13}>
                    O rascunho não teve cobertura factual suficiente no ditado. Revise e preencha manualmente antes de salvar.
                  </Typography>
                )}
                {aiReviewError && (
                  <Typography fontSize={13}>Confirme a revisão médica antes de salvar.</Typography>
                )}
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={aiDraft.reviewConfirmed}
                      disabled={isPending}
                      onChange={event => {
                        setAiDraft(current =>
                          current ? { ...current, reviewConfirmed: event.target.checked } : current
                        )
                        setAiReviewError(false)
                      }}
                    />
                  }
                  label="Revisei e confirmo o rascunho gerado pela IA"
                />
              </Stack>
            </Alert>
          )}

          <Section
            accent="primary"
            aiGenerated={aiDraft?.generated}
            complete={hasText(watchedFields.situation)}
            letter="S"
            title="Situação"
            subtitle="O que está acontecendo com o paciente agora."
          >
            <TextField
              id="field-situation"
              multiline
              minRows={3}
              variant="filled"
              label="Situação atual"
              placeholder="Ex.: Paciente internado por pneumonia, afebril nas últimas 24h, em ar ambiente."
              {...register('situation')}
              error={!!errors.situation}
              helperText={errors.situation?.message}
              {...voiceAdornment('situation', 'Situação atual')}
              disabled={isPending}
            />
            <Controller
              name="priority"
              control={control}
              render={({ field }) => {
                const selectedPriority = field.value ?? 'routine'

                return (
                  <Box>
                    <TextField
                      select
                      fullWidth
                      variant="filled"
                      label="Nível de atenção"
                      {...field}
                      value={selectedPriority}
                      disabled={isPending}
                    >
                      {priorityOptions.map(({ id, label, description }) => (
                        <MenuItem key={id} value={id}>
                          {label} - {description}
                        </MenuItem>
                      ))}
                    </TextField>
                    {errors.priority && <FormHelperText error>{errors.priority.message}</FormHelperText>}
                    <Chip
                      size="small"
                      label={priorityOptions.find(option => option.id === selectedPriority)?.label}
                      color={priorityColor[selectedPriority]}
                      sx={{ mt: 1 }}
                    />
                  </Box>
                )
              }}
            />
          </Section>

          <Section
            accent="info"
            aiGenerated={aiDraft?.generated}
            complete={hasText(watchedFields.background)}
            letter="B"
            title="Contexto"
            subtitle="Informações que explicam a internação e ajudam o próximo médico."
          >
            <TextField
              id="field-background"
              multiline
              minRows={3}
              variant="filled"
              label="Contexto clínico relevante"
              placeholder="Ex.: Diagnóstico principal, comorbidades importantes, tratamentos em andamento e eventos relevantes."
              {...register('background')}
              error={!!errors.background}
              helperText={errors.background?.message}
              {...voiceAdornment('background', 'Contexto clínico relevante')}
              disabled={isPending}
            />
          </Section>

          <Section
            accent="success"
            aiGenerated={aiDraft?.generated}
            complete={hasText(watchedFields.assessment)}
            letter="A"
            title="Avaliação"
            subtitle="Sua interpretação clínica e o que mudou desde a última visita."
          >
            <TextField
              id="field-assessment"
              multiline
              minRows={3}
              variant="filled"
              label="Avaliação clínica"
              placeholder="Ex.: Evolução estável, sem sinais de insuficiência respiratória, com melhora laboratorial parcial."
              {...register('assessment')}
              error={!!errors.assessment}
              helperText={errors.assessment?.message}
              {...voiceAdornment('assessment', 'Avaliação clínica')}
              disabled={isPending}
            />
            <Controller
              name="clinical_course"
              control={control}
              render={({ field }) => (
                <TextField
                  select
                  fullWidth
                  variant="filled"
                  label="Evolução em relação à última visita"
                  {...field}
                  value={field.value ?? ''}
                  disabled={isPending}
                >
                  <MenuItem value="">
                    Não informar agora
                  </MenuItem>
                  {clinicalCourseOptions.map(({ id, label }) => (
                    <MenuItem key={id} value={id}>
                      {label}
                    </MenuItem>
                  ))}
                </TextField>
              )}
            />
          </Section>

          <Section
            accent="warning"
            aiGenerated={aiDraft?.generated}
            complete={hasText(watchedFields.recommendation) || hasText(watchedFields.plan)}
            letter="R"
            title="Recomendação / Plano"
            subtitle="Conduta, próximos passos e pontos de atenção para continuidade do cuidado."
          >
            <TextField
              id="field-recommendation"
              multiline
              minRows={3}
              variant="filled"
              label="Recomendação"
              placeholder="Ex.: Manter antibiótico, fisioterapia respiratória, solicitar PCR amanhã e reavaliar oxigênio."
              {...register('recommendation')}
              error={!!errors.recommendation}
              helperText={errors.recommendation?.message}
              {...voiceAdornment('recommendation', 'Recomendação')}
              disabled={isPending}
            />
            <TextField
              id="field-plan"
              multiline
              minRows={2}
              variant="filled"
              label="Plano"
              placeholder="Ex.: Reavaliar amanhã com exames de controle e resposta clínica."
              {...register('plan')}
              error={!!errors.plan}
              helperText={errors.plan?.message}
              {...voiceAdornment('plan', 'Plano')}
              disabled={isPending}
            />
            <TextField
              id="field-pending-items"
              multiline
              minRows={2}
              variant="filled"
              label="Pendências para a equipe"
              placeholder="Ex.: Aguardar cultura, checar resposta do parecer da infectologia."
              {...register('pending_items')}
              error={!!errors.pending_items}
              helperText={errors.pending_items?.message}
              {...voiceAdornment('pending_items', 'Pendências para a equipe')}
              disabled={isPending}
            />
            <TextField
              id="field-alerts"
              multiline
              minRows={2}
              variant="filled"
              label="Alertas para o próximo médico"
              placeholder="Ex.: Se saturação ficar abaixo de 92%, avisar plantonista e considerar gasometria."
              {...register('alerts')}
              error={!!errors.alerts}
              helperText={errors.alerts?.message}
              {...voiceAdornment('alerts', 'Alertas para o próximo médico')}
              disabled={isPending}
            />
          </Section>

          <Section
            accent="info"
            complete={Boolean(images.length || existingImages.length)}
            letter="+"
            title="Anexos"
            subtitle="Adicione fotos ou documentos úteis para complementar a visita."
          >
            <InputImage onAddImage={(files: File[]) => setImages(prev => [...prev, ...files])} disabled={isPending} />
          </Section>
        </Stack>
      </Box>

      {(!!images.length || !!existingImages.length) && (
        <ImagesPreview
          images={[...existingImages, ...images]}
          onRemove={(item: number | Media) => {
            if (typeof item === 'number') {
              handleRemoveNew(existingImages.length - item)
            } else {
              handleRemoveExisting(item)
            }
          }}
          disabled={isPending}
        />
      )}
    </Stack>
  )
}

EvolutionForm.id = id
