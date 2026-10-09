import { Composition, Still } from "remotion";
import { HelloWorld } from "./HelloWorld";
import { PlasmoVideo } from "./plasmo/PlasmoVideo";
import { Thumbnail } from "./plasmo/Thumbnail";
import { PLATFORM, ShortVideo, type Platform, type ShortEdit } from "./plasmo/ShortVideo";
import shorts from "./plasmo/shorts.json";
import type { Edit } from "./plasmo/types";
import edit from "./plasmo/edit.json";

const plasmoEdit = edit as Edit;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="PlasmoVideo"
        component={PlasmoVideo}
        durationInFrames={Math.ceil(plasmoEdit.duration * plasmoEdit.fps)}
        fps={plasmoEdit.fps}
        width={1920}
        height={1080}
        defaultProps={{ edit: plasmoEdit }}
      />
      {(shorts as unknown as ShortEdit[]).flatMap((sh) =>
        (["tiktok", "reels", "shorts"] as Platform[]).map((platform) => (
          <Composition
            key={`${sh.id}-${platform}`}
            id={`${sh.id}-${platform}`}
            component={ShortVideo}
            durationInFrames={Math.ceil((sh.talk + PLATFORM[platform].ctaSeconds) * sh.fps)}
            fps={sh.fps}
            width={1080}
            height={1920}
            defaultProps={{ edit: sh, platform }}
          />
        )),
      )}
      <Still id="Thumbnail" component={Thumbnail} width={1920} height={1080} />
    </>
  );
};
