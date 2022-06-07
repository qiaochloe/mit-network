import { ResponsiveNetwork } from '@nivo/network'

const CourseNetwork = ({ data }) => (
  <ResponsiveNetwork
    // base
    data={data}
    margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
    // simulation
    centeringStrength={0.3}
    repulsivity={6}
    // nodes
    // links
    motionConfig="wobbly"
    // interactivity
  />
);

export default CourseNetwork