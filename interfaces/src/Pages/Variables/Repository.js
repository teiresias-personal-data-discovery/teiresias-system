import { Input, Tooltip } from 'antd';
import _ from 'lodash';
import { WarningOutlined } from '@ant-design/icons';
import styled from 'styled-components';

import Flex from '../../Base/Flex';
import Card from '../../Base/Card';
import { colors } from '../../Base/constants';
import { Error } from '../../Base/Login';
import ErrorBoundary from '../../Base/ErrorBoundary';

export const Wrapper = styled(Flex)`
  width: 100vw;
  margin-top: 10px;
`;
const ErrorWrapper = styled(Flex)`
  width: 100%;
`;
const Title = styled(Flex)`
  margin: 0 10px 0 15px;
  width: 90px;
`;
const Uri = styled(Title)``;
const UriWrapper = styled(Flex)`
  width: 450px;
`;
const DefaultWrapper = styled(Flex)`
  width: 200px;
`;
const ErrorIcon = styled(WarningOutlined)`
  font-size: 16px;
  color: ${colors.error};
`;

const gitError = (
  dateString
) => `This repository wasn't accessible in the last discovery run at ${dateString}.
                  You can check the logs of Airflow for details on the error.`;

const Repository = ({
  repositoryName,
  values,
  setPending,
  pendingChanges,
  evalErrors,
}) => (
  <ErrorBoundary domain="repository info" key={repositoryName}>
    <Card
      title={repositoryName}
      info={
        values.last_run_errored_at && (
          <Tooltip title={gitError(values.last_run_errored_at)}>
            <ErrorIcon />
          </Tooltip>
        )
      }
    >
      <Flex space>
        <Uri align="center">Git SSH-URI:</Uri>
        <UriWrapper>
          <Input
            id="uri"
            size="small"
            value={_.get(pendingChanges, [repositoryName, 'uri']) ?? values.uri}
            onChange={setPending(repositoryName)}
          />
        </UriWrapper>
      </Flex>
      <Flex>
        <Title align="center">Branch:</Title>
        <DefaultWrapper>
          <Input
            id="branch"
            size="small"
            value={
              _.get(pendingChanges, [repositoryName, 'branch']) ?? values.branch
            }
            onChange={setPending(repositoryName)}
          />
        </DefaultWrapper>
      </Flex>

      {_.get(evalErrors, repositoryName) && (
        <ErrorWrapper align="flex-start" end>
          <Error>{_.get(evalErrors, repositoryName)}</Error>
        </ErrorWrapper>
      )}
    </Card>
  </ErrorBoundary>
);

export default Repository;
