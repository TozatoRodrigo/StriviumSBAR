import { useRef, useState } from 'react'

export type AudioRecord = {
  isRecording: boolean
  audioBlob: Blob | null
  audioURL: string | null
  startRecording: () => Promise<void>
  stopRecording: () => void
  resetRecording: () => void
}

export function useAudioRecorder(): AudioRecord {
  const [isRecording, setIsRecording] = useState(false)
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [audioURL, setAudioURL] = useState<string | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mediaRecorder = new MediaRecorder(stream)
    mediaRecorderRef.current = mediaRecorder
    audioChunksRef.current = []

    mediaRecorder.ondataavailable = event => {
      audioChunksRef.current.push(event.data)
    }

    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
      setAudioBlob(blob)
      setAudioURL(URL.createObjectURL(blob))
    }

    mediaRecorder.start()
    setIsRecording(true)
  }

  function stopRecording() {
    mediaRecorderRef.current?.stop()
    setIsRecording(false)
  }

  function resetRecording() {
    setAudioBlob(null)
    setAudioURL(null)
    audioChunksRef.current = []
  }

  return {
    isRecording,
    audioBlob,
    audioURL,
    startRecording,
    stopRecording,
    resetRecording,
  }
}
