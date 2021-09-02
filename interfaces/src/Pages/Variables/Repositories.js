import { useState, useCallback, useEffect, useMemo } from 'react';
import { notification, Empty } from 'antd';
import _ from 'lodash';
import styled from 'styled-components';

import Flex from '../../Base/Flex';
import Buttons from '../Buttons';
import Repository from './Repository';

export const Wrapper = styled(Flex)`
  width: 100vw;
  margin-top: 10px;
`;

const NoData = styled(Empty)`
  .ant-empty-description {
    color: white;
  }
`;

const isValidRepositoryUri = (repositoryUri) => {
  if (
    !_.startsWith(repositoryUri, 'git@') ||
    !_.endsWith(repositoryUri, '.git')
  ) {
    return false;
  }
  return true;
};

const getRepositoryName = (repositoryUri) => {
  return _.chain(repositoryUri)
    .split(':')
    .last()
    .value()
    .slice(0, -4)
    .replaceAll(/[\W_]+/g, '.');
};

const Repositories = ({
  repositories,
  isLoading,
  variablesError,
  fetchRepositories,
  postRepositories,
  variablesStatus,
}) => {
  const [pendingChanges, setPendingChanges] = useState({});
  const [evalErrors, setEvalErrors] = useState({});

  const setPending = useCallback(
    (key) => (value) => {
      setPendingChanges((prev) => ({
        ...prev,
        [key]: {
          ..._.get(prev, key, {}),
          [value.target.id]: value.target.value,
        },
      }));
    },
    [setPendingChanges]
  );

  const addRepository = useCallback(() => {
    setPending(new Date().getTime())({ target: { id: 'uri', value: '' } });
  }, [setPending]);

  const updateRepositories = useCallback(() => {
    const { newRepositories, errors } = _.reduce(
      pendingChanges,
      (result, pendingChangesObject, name) => {
        let newResult = { ...result };
        const uri = _.get(pendingChangesObject, 'uri');
        if (uri && !isValidRepositoryUri(uri)) {
          _.set(newResult, ['errors', name], 'uri invalid');
          return newResult;
        }
        const newValues = {
          ..._.get(repositories, name),
          ...pendingChangesObject,
        };
        if (!_.isEmpty(_.difference(['uri', 'branch'], _.keys(newValues)))) {
          _.set(newResult, ['errors', name], 'missing value');
          return newResult;
        }
        if (uri) {
          const newRepositoryName = getRepositoryName(uri);
          if (_.get(repositories, newRepositoryName)) {
            _.set(newResult, ['errors', name], 'duplicate repository');
            return newResult;
          }
          _.set(newResult, ['newRepositories', newRepositoryName], newValues);
          _.unset(newResult, ['newRepositories', name]);
        } else {
          _.set(newResult, ['newRepositories', name], newValues);
        }
        return newResult;
      },
      {
        newRepositories: { ...repositories },
        errors: {},
      }
    );
    if (_.isEmpty(errors)) {
      postRepositories(newRepositories);
      setEvalErrors({});
    } else {
      setEvalErrors(errors);
    }
  }, [pendingChanges, repositories, postRepositories]);

  const consolidatedRepositories = useMemo(() => {
    if (!_.isEmpty(repositories) || !_.isEmpty(pendingChanges)) {
      return { ...pendingChanges, ...repositories };
    }
    return {};
  }, [repositories, pendingChanges]);

  const openNotification = useCallback((status) => {
    if (status === 'success') {
      notification.success({
        message: `Successfully updated Repositories`,
        description: '',
      });
    }
    if (status === 'error') {
      notification.info({
        message: `Something went wrong`,
        description: '',
      });
    }
  }, []);

  useEffect(() => {
    if (variablesStatus === 'success') {
      openNotification('success');
      setPendingChanges({});
    }
    if (variablesStatus === 'error') {
      openNotification('error');
    }
  }, [variablesStatus, openNotification]);

  return (
    <Wrapper column align="center">
      <Buttons
        add={addRepository}
        save={!_.isEmpty(pendingChanges) && updateRepositories}
        isLoading={isLoading}
        error={variablesError}
        fetch={fetchRepositories}
      />
      {_.isEmpty(consolidatedRepositories) ? (
        <NoData
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          description="No Repositories"
        />
      ) : (
        _.map(consolidatedRepositories, (values, repositoryName) => (
          <Repository
            repositoryName={repositoryName}
            values={values}
            setPending={setPending}
            pendingChanges={pendingChanges}
            evalErrors={evalErrors}
          />
        ))
      )}
    </Wrapper>
  );
};

export default Repositories;
