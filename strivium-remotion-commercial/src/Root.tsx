import "./index.css";
import { Composition } from "remotion";
import { MyComposition, getCommercialDurationInFrames } from "./Composition";

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="StriviumCommercial"
        component={MyComposition}
        durationInFrames={getCommercialDurationInFrames(FPS)}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </>
  );
};
