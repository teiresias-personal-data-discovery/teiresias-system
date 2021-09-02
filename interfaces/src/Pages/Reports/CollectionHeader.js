import _ from 'lodash';
import styled from 'styled-components';
import { Progress } from 'antd';
import { AlertOutlined } from '@ant-design/icons';

import Flex from '../../Base/Flex';
import { colors } from '../../Base/constants';

import Summary from './Summary';

export const Highlight = styled.span`
  font-style: italic;
  padding-left: 0.3em;
  padding-right: 0.3em;
`;

export const StorageName = styled.span`
  color: ${colors.tertiary};
  font-size: 20px;
  font-style: italic;
  padding-bottom: 5px;
  line-height: 1em;
  width: 200px;
`;

const Wrapper = styled(Flex)`
  margin: 0 20px;
  width: 400px;
`;

const Header = styled(Flex)`
  margin: 10px 0;
`;

const Scala = styled(Progress)`
  width: 400px;
`;

const Alert = styled(AlertOutlined)`
  color: ${colors.error};
  margin-left: 10px;
`;

const gradient = {
  '0%': 'darkgrey',
  '100%': colors.error,
};

const CollectionHeader = ({
  collectionName,
  collectionSummary,
  isJSONReport,
}) => (
  <>
    <Header space>
      <StorageName>{collectionName}</StorageName>
      <Wrapper>
        <Scala
          strokeColor={gradient}
          percent={_.get(collectionSummary, 'collectionMetric') * 100}
          showInfo={false}
        />
        {_.get(collectionSummary, 'collectionMetric') > 0 && <Alert />}
      </Wrapper>
    </Header>
    <Summary summary={collectionSummary} isJSONReport />
  </>
);

export default CollectionHeader;
