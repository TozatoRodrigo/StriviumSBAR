'use client'

import { Box, Chip, FormHelperText, MenuItem, Stack, TextField, Typography } from '@mui/material'
import { useMemo, useState, type ReactNode } from 'react'
import { useAudioRecorder } from '@/hooks/useAudioRecorder'
import { AudioControllers } from './AudioControllers'
import { AudioPreview } from './AudioPreview'
import { ImagesPreview } from './ImagesPreview'
import { InputImage } from './InputImage'
import { Controller, useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import {
  clinicalCourseOptions,
  defaultEvolutionType,
  priorityOptions,
} from '@/constants/evolutions'
import { EvolutionFormData, EvolutionSchema } from '@/validations/evolution'
import { EvolutionSbar, Media } from '@/hooks/queries/evolutions'
import { useResetOnDataChange } from '@/hooks/useResetOnDataChange'

type EvolutionFormInitialData = Partial<EvolutionFormData> & {
  description?: string
  medias?: Media[]
  sbar?: EvolutionSbar | null
}

type EvolutionFormProps = {
  formId?: string
  initialData?: EvolutionFormInitialData
  submitAction: (payload: FormData) => void
  isPending: boolean
}

const id = 'evolution-form'

const normalizeInitialData = (initialData?: EvolutionFormInitialData): EvolutionFormData => ({
  type: initialData?.type ?? defaultEvolutionType,
  situation: initialData?.situation ?? initialData?.sbar?.situation ?? initialData?.description ?? '',
  background: initialData?.background ?? initialData?.sbar?.background ?? '',
  assessment: initialData?.assessment ?? initialData?.sbar?.assessment ?? '',
  recommendation: initialData?.recommendation ?? initialData?.sbar?.recommendation ?? '',
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
    `Plano: ${data.recommendation.trim()}`,
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

const Section = ({ title, subtitle, children }: { title: string; subtitle: string; children: ReactNode }) => (
  <Box
    sx={{
      border: theme => `1px solid ${theme.palette.divider}`,
      borderRadius: 2,
      p: { xs: 2, sm: 2.5 },
      bgcolor: 'background.paper',
    }}
  >
    <Box sx={{ mb: 2 }}>
      <Typography fontWeight={700} color="text.primary">
        {title}
      </Typography>
      <Typography fontSize={13} color="text.secondary">
        {subtitle}
      </Typography>
    </Box>
    <Stack gap={2}>{children}</Stack>
  </Box>
)

export const EvolutionForm = ({
  formId = id,
  submitAction,
  isPending,
  initialData,
}: EvolutionFormProps) => {
  const { isRecording, audioBlob, audioURL, startRecording, stopRecording, resetRecording } = useAudioRecorder()
  const normalizedInitialData = useMemo(() => normalizeInitialData(initialData), [initialData])
  const [images, setImages] = useState<File[]>([])
  const [existingImages, setExistingImages] = useState<Media[]>(
    initialData?.medias?.filter(m => m.type === 'photo') ?? []
  )
  const [removedImages, setRemovedImages] = useState<string[]>([])

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
    reset,
    formState: { errors },
  } = useForm<EvolutionFormData>({
    resolver: zodResolver(EvolutionSchema),
    defaultValues: normalizedInitialData,
  })

  const onSubmit = async (data: EvolutionFormData) => {
    const formData = new FormData()
    const description = buildSbarDescription(data)

    formData.append('description', description)
    formData.append('action_type', defaultEvolutionType)
    formData.append('sbar_situation', data.situation.trim())
    appendIfFilled(formData, 'sbar_background', data.background)
    formData.append('sbar_assessment', data.assessment.trim())
    formData.append('sbar_recommendation', data.recommendation.trim())
    formData.append('sbar_priority', data.priority)
    appendIfFilled(formData, 'sbar_clinical_course', data.clinical_course)
    appendIfFilled(formData, 'sbar_pending_items', data.pending_items)
    appendIfFilled(formData, 'sbar_alerts', data.alerts)

    if (audioBlob) {
      formData.append('files', audioBlob, 'recording.webm')
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
      sx={{ overflowY: 'auto', pb: 3 }}
    >
      <Box sx={{ maxWidth: 980, width: '100%', mx: 'auto' }}>
        <Stack gap={2.5}>
          <Box>
            <Typography fontSize={13} color="text.secondary">
              Use o SBAR para registrar uma visita objetiva, fácil de continuar no próximo plantão.
            </Typography>
            <Stack direction="row" gap={1} flexWrap="wrap" sx={{ mt: 1 }}>
              <Chip label="Visita médica" size="small" color="primary" variant="outlined" />
              <Chip label="SBAR estruturado" size="small" color="info" variant="outlined" />
            </Stack>
          </Box>

          <Section title="S - Situação" subtitle="O que está acontecendo com o paciente agora.">
            <TextField
              multiline
              minRows={3}
              variant="filled"
              label="Situação atual"
              placeholder="Ex.: Paciente internado por pneumonia, afebril nas últimas 24h, em ar ambiente."
              {...register('situation')}
              error={!!errors.situation}
              helperText={errors.situation?.message}
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

          <Section title="B - Contexto" subtitle="Informações que explicam a internação e ajudam o próximo médico.">
            <TextField
              multiline
              minRows={3}
              variant="filled"
              label="Contexto clínico relevante"
              placeholder="Ex.: Diagnóstico principal, comorbidades importantes, tratamentos em andamento e eventos relevantes."
              {...register('background')}
              error={!!errors.background}
              helperText={errors.background?.message}
              disabled={isPending}
            />
          </Section>

          <Section title="A - Avaliação" subtitle="Sua interpretação clínica e o que mudou desde a última visita.">
            <TextField
              multiline
              minRows={3}
              variant="filled"
              label="Avaliação clínica"
              placeholder="Ex.: Evolução estável, sem sinais de insuficiência respiratória, com melhora laboratorial parcial."
              {...register('assessment')}
              error={!!errors.assessment}
              helperText={errors.assessment?.message}
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

          <Section title="R - Recomendação / Plano" subtitle="Conduta, próximos passos e pontos de atenção para continuidade do cuidado.">
            <TextField
              multiline
              minRows={3}
              variant="filled"
              label="Plano e conduta"
              placeholder="Ex.: Manter antibiótico, fisioterapia respiratória, solicitar PCR amanhã e reavaliar oxigênio."
              {...register('recommendation')}
              error={!!errors.recommendation}
              helperText={errors.recommendation?.message}
              disabled={isPending}
            />
            <TextField
              multiline
              minRows={2}
              variant="filled"
              label="Pendências para a equipe"
              placeholder="Ex.: Aguardar cultura, checar resposta do parecer da infectologia."
              {...register('pending_items')}
              error={!!errors.pending_items}
              helperText={errors.pending_items?.message}
              disabled={isPending}
            />
            <TextField
              multiline
              minRows={2}
              variant="filled"
              label="Alertas para o próximo médico"
              placeholder="Ex.: Se saturação ficar abaixo de 92%, avisar plantonista e considerar gasometria."
              {...register('alerts')}
              error={!!errors.alerts}
              helperText={errors.alerts?.message}
              disabled={isPending}
            />
          </Section>

          <Section title="Anexos" subtitle="Adicione fotos ou documentos úteis para complementar a visita.">
            <InputImage onAddImage={(files: File[]) => setImages(prev => [...prev, ...files])} disabled={isPending} />

            {
              /* TODO[v1]: enable */
              !!0 && (
                <AudioControllers
                  isRecording={isRecording}
                  startRecording={startRecording}
                  stopRecording={stopRecording}
                  resetRecording={resetRecording}
                  hasBlob={!!audioBlob}
                  disabled={isPending}
                />
              )
            }
          </Section>
        </Stack>
      </Box>

      {audioURL && <AudioPreview audioURL={audioURL} />}
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
