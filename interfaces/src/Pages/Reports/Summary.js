import _ from 'lodash';
import styled from 'styled-components';

import { colors } from '../../Base/constants';

const Meta = styled.div`
  padding: 5px;
  border: 1px solid ${colors.tertiary};
  color: ${colors.tertiary};
`;

const Metric = styled.span`
  font-size: 0.9em;
  font-style: italic;
`;
const Teiresias = styled.span`
  font-size: 1.5em;

  font-style: italic;
`;

const titles = {
  collectionMetric: (value) => (
    <div>
      <Teiresias>Teiresias</Teiresias>
      <Metric>metric</Metric>: {value}
    </div>
  ),
  numberOfEntities: (value, isJSONReport) => (
    <div>Number of entities: {isJSONReport ? '>=1' : value}</div>
  ),
  hasDataMatches: (value) => (
    <div>
      Has data matches:
      {value === true ? ' True' : ' False'}
    </div>
  ),
  meanProximities: (value) => (
    <div>Mean of attribute-to-lookup proximities: {value * 100}%</div>
  ),
};

const Summary = ({ summary, isJSONReport }) => (
  <Meta>
    <ul>
      {_.map(titles, (factory, key) =>
        factory(_.get(summary, key, ''), isJSONReport)
      )}
    </ul>
  </Meta>
);

export default Summary;
