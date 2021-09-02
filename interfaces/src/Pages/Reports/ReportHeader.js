import moment from 'moment';
import { FaCode, FaDatabase } from 'react-icons/fa';
import { VscJson } from 'react-icons/vsc';
import { DiGitBranch } from 'react-icons/di';
import { Avatar, Badge } from 'antd';
import styled from 'styled-components';
import { AlertOutlined } from '@ant-design/icons';

import Flex from '../../Base/Flex';
import { colors, personalDataMessage } from '../../Base/constants';

const HeaderRow = styled(Flex)`
  width: 100%;
`;

const IndicatorRow = styled(HeaderRow)`
  margin-top: 15px;
  > * {
    margin-right: 10px;
  }
`;

const Indicator = styled(Avatar)`
  margin-left: 10px;
`;

const Time = styled(Flex)`
  width: 500px;
`;

const Summary = styled(Flex)`
  padding: 5px 0 0 15px;
  width: 100%;
  font-size: 15px;
`;

const Count = styled(Badge)`
  .ant-badge-count {
    background: ${colors.primary};
  }
`;

const Alert = styled(AlertOutlined)`
  color: ${colors.error};
  margin-left: 10px;
`;

const Header = ({
  date,
  numberOfRepoCodeAnalysis,
  hasManuallyCodeAnalysis,
  numberOfStorageDataAnalysis,
  hasJSONDataAnalysis,
  hasPersonalDataMatch,
}) => (
  <Flex column>
    <HeaderRow align="space">
      <Time>{moment(date).format('YYYY MMMM Do , hh:mm')}</Time>
      <Summary column>
        {hasPersonalDataMatch && (
          <Flex>
            {personalDataMessage}
            <Alert />
          </Flex>
        )}
      </Summary>
    </HeaderRow>
    <IndicatorRow align="space">
      {hasManuallyCodeAnalysis > 0 && (
        <Count count={1}>
          <Indicator size="small" icon={<FaCode />} />
        </Count>
      )}
      {numberOfRepoCodeAnalysis > 0 && (
        <Count count={numberOfRepoCodeAnalysis}>
          <Indicator size="small" icon={<DiGitBranch />} />
        </Count>
      )}
      {numberOfStorageDataAnalysis > 0 && (
        <Count count={numberOfStorageDataAnalysis}>
          <Indicator size="small" icon={<FaDatabase />} />
        </Count>
      )}
      {hasJSONDataAnalysis > 0 && (
        <Count count={1}>
          <Indicator size="small" icon={<VscJson />} />
        </Count>
      )}
    </IndicatorRow>
  </Flex>
);

export default Header;
