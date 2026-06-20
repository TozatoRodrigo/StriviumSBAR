import { Audio, Video } from "@remotion/media";
import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const SOURCE_VIDEO_FILE = "strivium-link-source-cropped.mp4";
const BGM_FILE = "strivium-commercial-bgm-animated.wav";

const TIMING = {
  normalEndSeconds: 30,
  acceleratedStartSeconds: 30,
  acceleratedEndSeconds: 56,
  acceleratedPlaybackRate: 2,
};

const SOURCE_DURATION_SECONDS = 92.816667;
const SCREEN_OVERSCAN = 1.035;

export const getCommercialDurationInFrames = (fps: number) => {
  const normalFrames = Math.round(TIMING.normalEndSeconds * fps);
  const acceleratedSourceFrames = Math.round(
    (TIMING.acceleratedEndSeconds - TIMING.acceleratedStartSeconds) * fps,
  );
  const sourceDurationFrames = Math.round(SOURCE_DURATION_SECONDS * fps);
  const acceleratedEndFrame = Math.round(TIMING.acceleratedEndSeconds * fps);
  const tailFrames = Math.max(0, sourceDurationFrames - acceleratedEndFrame);

  return (
    normalFrames +
    Math.floor(acceleratedSourceFrames / TIMING.acceleratedPlaybackRate) +
    tailFrames
  );
};

export const MyComposition = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const normalFrames = Math.round(TIMING.normalEndSeconds * fps);
  const acceleratedFrames = Math.floor(
    ((TIMING.acceleratedEndSeconds - TIMING.acceleratedStartSeconds) * fps) /
      TIMING.acceleratedPlaybackRate,
  );
  const acceleratedEndFrame = Math.round(TIMING.acceleratedEndSeconds * fps);
  const sourceDurationFrames = Math.round(SOURCE_DURATION_SECONDS * fps);
  const tailFrames = Math.max(0, sourceDurationFrames - acceleratedEndFrame);

  const entrance = interpolate(frame, [0, 40], [0, 1], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const phoneScale = interpolate(entrance, [0, 1], [0.92, 1]);
  const phoneYOffset = interpolate(entrance, [0, 1], [40, 0]);

  const glowPulse = 0.85 + Math.sin((frame / fps) * 2.6) * 0.15;
  const sweepCycle = (frame % (fps * 4)) / (fps * 4);
  const sweepX = interpolate(sweepCycle, [0, 1], [-640, 920]);
  const featureFloat = Math.sin((frame / fps) * 1.7) * 7;

  const headlineIn = interpolate(frame, [0, 45], [0, 1], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const featureIn = interpolate(frame, [18, 72], [0, 1], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const outroStart = Math.max(0, durationInFrames - Math.round(fps * 4.3));
  const outroProgress = interpolate(
    frame,
    [outroStart, durationInFrames - 1],
    [0, 1],
    {
      easing: Easing.bezier(0.16, 1, 0.3, 1),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  const bgmFadeIn = interpolate(frame, [0, Math.round(fps * 2)], [0, 0.3], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const bgmFadeOut = interpolate(
    frame,
    [Math.max(0, durationInFrames - Math.round(fps * 3)), durationInFrames - 1],
    [1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.bezier(0.5, 0, 0.8, 0.2),
    },
  );
  const bgmVolume = bgmFadeIn * bgmFadeOut;

  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(circle at 15% 20%, #0c2d7f 0%, #07153f 35%, #020811 70%, #01040a 100%)",
        overflow: "hidden",
      }}
    >
      <Audio src={staticFile(BGM_FILE)} volume={bgmVolume} />

      <div
        style={{
          position: "absolute",
          inset: -320,
          background:
            "radial-gradient(circle at 18% 30%, rgba(57,129,255,0.45) 0%, rgba(57,129,255,0) 48%)",
          filter: "blur(35px)",
          transform: `scale(${glowPulse})`,
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 900,
          height: 900,
          right: -260,
          bottom: -260,
          borderRadius: "50%",
          background:
            "radial-gradient(circle, rgba(35,111,255,0.5) 0%, rgba(35,111,255,0) 67%)",
          filter: "blur(24px)",
          opacity: 0.9,
        }}
      />

      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: 66,
            left: 88,
            width: 560,
            opacity: headlineIn,
            transform: `translateY(${interpolate(headlineIn, [0, 1], [22, 0])}px)`,
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 10,
              borderRadius: 999,
              padding: "10px 18px",
              background:
                "linear-gradient(90deg, rgba(30,117,255,0.85) 0%, rgba(82,162,255,0.92) 100%)",
              boxShadow: "0 12px 32px rgba(24,100,255,0.35)",
              color: "#eaf4ff",
              fontSize: 15,
              letterSpacing: 1.4,
              fontWeight: 700,
              textTransform: "uppercase",
              fontFamily: "Avenir Next, Helvetica Neue, Arial, sans-serif",
            }}
          >
            <span
              style={{
                width: 9,
                height: 9,
                borderRadius: "50%",
                background: "#dff0ff",
                boxShadow: "0 0 10px rgba(223,240,255,0.95)",
              }}
            />
            Novo comercial
          </div>
          <div
            style={{
              marginTop: 16,
              color: "#eef6ff",
              fontSize: 56,
              lineHeight: 1.02,
              fontWeight: 800,
              letterSpacing: -1.2,
              fontFamily: "Avenir Next, Helvetica Neue, Arial, sans-serif",
              textShadow: "0 16px 45px rgba(7,24,62,0.48)",
            }}
          >
            Visitas clinicas
            <br />
            em segundos
          </div>
          <div
            style={{
              marginTop: 14,
              color: "rgba(211,228,255,0.98)",
              fontSize: 23,
              lineHeight: 1.35,
              maxWidth: 500,
              fontWeight: 500,
              fontFamily: "Avenir Next, Helvetica Neue, Arial, sans-serif",
            }}
          >
            Strivium Link acelera registro, conduta e colaboracao em tempo real.
          </div>
        </div>

        <div
          style={{
            position: "absolute",
            left: 116,
            top: 430 + featureFloat,
            width: 330,
            borderRadius: 22,
            padding: "18px 20px",
            background:
              "linear-gradient(180deg, rgba(15,66,170,0.45) 0%, rgba(6,30,84,0.55) 100%)",
            border: "1px solid rgba(146,193,255,0.38)",
            boxShadow: "0 16px 38px rgba(7,26,72,0.42)",
            color: "#e6f2ff",
            opacity: featureIn * (1 - outroProgress),
            transform: `translateX(${interpolate(featureIn, [0, 1], [-26, 0])}px)`,
          }}
        >
          <div
            style={{
              fontSize: 16,
              textTransform: "uppercase",
              letterSpacing: 1.4,
              fontWeight: 700,
              color: "#9cc7ff",
              fontFamily: "Avenir Next, Helvetica Neue, Arial, sans-serif",
            }}
          >
            Fluxo inteligente
          </div>
          <div
            style={{
              marginTop: 8,
              fontSize: 24,
              lineHeight: 1.2,
              fontWeight: 700,
              fontFamily: "Avenir Next, Helvetica Neue, Arial, sans-serif",
            }}
          >
            Registro com IA
            <br />
            direto no plantao
          </div>
        </div>

        <div
          style={{
            position: "absolute",
            right: 116,
            top: 500 - featureFloat,
            width: 318,
            borderRadius: 22,
            padding: "18px 20px",
            background:
              "linear-gradient(180deg, rgba(12,86,206,0.45) 0%, rgba(8,37,101,0.58) 100%)",
            border: "1px solid rgba(146,193,255,0.38)",
            boxShadow: "0 16px 38px rgba(7,26,72,0.42)",
            color: "#e6f2ff",
            opacity: featureIn * (1 - outroProgress),
            transform: `translateX(${interpolate(featureIn, [0, 1], [26, 0])}px)`,
          }}
        >
          <div
            style={{
              fontSize: 16,
              textTransform: "uppercase",
              letterSpacing: 1.4,
              fontWeight: 700,
              color: "#9cc7ff",
              fontFamily: "Avenir Next, Helvetica Neue, Arial, sans-serif",
            }}
          >
            Decisao rapida
          </div>
          <div
            style={{
              marginTop: 8,
              fontSize: 24,
              lineHeight: 1.2,
              fontWeight: 700,
              fontFamily: "Avenir Next, Helvetica Neue, Arial, sans-serif",
            }}
          >
            Menos burocracia,
            <br />
            mais tempo ao paciente
          </div>
        </div>

        <div
          style={{
            position: "relative",
            width: 470,
            height: 930,
            borderRadius: 72,
            padding: 14,
            background:
              "linear-gradient(145deg, #f8fbff 0%, #b3c7e8 28%, #293448 52%, #899cbf 75%, #d6e6ff 100%)",
            boxShadow:
              "0 0 0 1px rgba(255,255,255,0.45), 0 28px 90px rgba(14,101,255,0.45), 0 6px 28px rgba(0,0,0,0.55)",
            transform: `translateY(${phoneYOffset}px) scale(${phoneScale})`,
          }}
        >
          <div
            style={{
              position: "absolute",
              top: 24,
              left: 24,
              right: 24,
              height: 16,
              borderRadius: 999,
              background: "rgba(255,255,255,0.55)",
              filter: "blur(8px)",
              opacity: 0.7,
            }}
          />

          <div
            style={{
              position: "relative",
              width: "100%",
              height: "100%",
              borderRadius: 58,
              overflow: "hidden",
              backgroundColor: "#edf3fb",
            }}
          >
            <Sequence durationInFrames={normalFrames}>
              <Video
                src={staticFile(SOURCE_VIDEO_FILE)}
                trimAfter={normalFrames}
                objectFit="cover"
                muted
                style={{
                  width: "100%",
                  height: "100%",
                  transform: `scale(${SCREEN_OVERSCAN})`,
                  transformOrigin: "center center",
                }}
              />
            </Sequence>

            <Sequence from={normalFrames} durationInFrames={acceleratedFrames}>
              <Video
                src={staticFile(SOURCE_VIDEO_FILE)}
                trimBefore={TIMING.acceleratedStartSeconds * fps}
                trimAfter={TIMING.acceleratedEndSeconds * fps}
                playbackRate={TIMING.acceleratedPlaybackRate}
                objectFit="cover"
                muted
                style={{
                  width: "100%",
                  height: "100%",
                  transform: `scale(${SCREEN_OVERSCAN})`,
                  transformOrigin: "center center",
                }}
              />
            </Sequence>

            <Sequence
              from={normalFrames + acceleratedFrames}
              durationInFrames={tailFrames}
            >
              <Video
                src={staticFile(SOURCE_VIDEO_FILE)}
                trimBefore={acceleratedEndFrame}
                objectFit="cover"
                muted
                style={{
                  width: "100%",
                  height: "100%",
                  transform: `scale(${SCREEN_OVERSCAN})`,
                  transformOrigin: "center center",
                }}
              />
            </Sequence>

            <div
              style={{
                position: "absolute",
                inset: 0,
                background:
                  "radial-gradient(circle at 50% 10%, rgba(101,179,255,0.26) 0%, rgba(33,121,255,0.2) 30%, rgba(6,24,66,0.18) 100%)",
                mixBlendMode: "screen",
              }}
            />
            <div
              style={{
                position: "absolute",
                top: -220,
                left: sweepX,
                width: 560,
                height: 1400,
                transform: "rotate(22deg)",
                background:
                  "linear-gradient(90deg, rgba(255,255,255,0) 8%, rgba(125,196,255,0.24) 50%, rgba(255,255,255,0) 92%)",
                filter: "blur(2px)",
                pointerEvents: "none",
              }}
            />

            <div
              style={{
                position: "absolute",
                top: 24,
                left: "50%",
                width: 150,
                height: 38,
                transform: "translateX(-50%)",
                borderRadius: 24,
                background:
                  "linear-gradient(180deg, rgba(0,0,0,0.95) 0%, rgba(8,12,22,0.92) 100%)",
                boxShadow:
                  "0 0 0 1px rgba(255,255,255,0.08), 0 10px 24px rgba(0,0,0,0.45)",
              }}
            />
          </div>
        </div>

        <div
          style={{
            position: "absolute",
            bottom: 60,
            left: "50%",
            transform: "translateX(-50%)",
            padding: "16px 34px",
            borderRadius: 999,
            background:
              "linear-gradient(90deg, rgba(24,105,255,0.86) 0%, rgba(87,165,255,0.92) 100%)",
            boxShadow: "0 20px 48px rgba(11,76,196,0.42)",
            color: "#eff7ff",
            fontSize: 24,
            letterSpacing: 0.2,
            fontWeight: 700,
            fontFamily: "Avenir Next, Helvetica Neue, Arial, sans-serif",
            opacity: 1 - outroProgress,
          }}
        >
          Mais agilidade. Menos retrabalho.
        </div>

        <div
          style={{
            position: "absolute",
            inset: 0,
            opacity: outroProgress,
            background:
              "linear-gradient(180deg, rgba(2,8,20,0) 0%, rgba(2,8,20,0.72) 45%, rgba(2,8,20,0.95) 100%)",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: 92,
            left: 120,
            right: 120,
            textAlign: "center",
            color: "#f0f7ff",
            opacity: outroProgress,
            transform: `translateY(${interpolate(outroProgress, [0, 1], [24, 0])}px)`,
            fontFamily: "Avenir Next, Helvetica Neue, Arial, sans-serif",
          }}
        >
          <div
            style={{
              fontSize: 58,
              lineHeight: 1.05,
              fontWeight: 800,
              textShadow: "0 18px 42px rgba(0,0,0,0.5)",
            }}
          >
            Strivium Link
          </div>
          <div
            style={{
              marginTop: 8,
              fontSize: 30,
              lineHeight: 1.2,
              fontWeight: 600,
              color: "rgba(214,231,255,0.98)",
            }}
          >
            Performance clinica em cada visita.
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
