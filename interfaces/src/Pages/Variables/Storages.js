import { useState, useCallback, useEffect, useMemo } from 'react';
import _ from 'lodash';
import { notification, Empty } from 'antd';
import styled from 'styled-components';

import Storage from './Storage';
import Buttons from '../Buttons';
import ErrorBoundary from '../../Base/ErrorBoundary';
import { Wrapper } from './Repositories';

const NoData = styled(Empty)`
  .ant-empty-description {
    color: white;
  }
`;

const Storages = ({
  storageCredentials,
  variablesStatus,
  isLoading,
  variablesError,
  fetchStorageCredentials,
  postStorageCredentials,
}) => {
  const [pendingChanges, setPendingChanges] = useState({});
  const setPending = useCallback(
    (storageKey) => (valueKey, value, removeKey) => {
      setPendingChanges((prev) => {
        let prevStorage = _.get(prev, storageKey, {});
        if (removeKey) {
          _.set(prevStorage, removeKey, null);
        }
        return {
          ...prev,
          [storageKey]: {
            ...prevStorage,
            [valueKey]: value,
          },
        };
      });
    },
    [setPendingChanges]
  );

  const setPendingInput = useCallback(
    (key) => (value) => {
      // for internal usage, the identifier can't consist of special characters
      let newValue = value.target.value;
      if (key === 'storageIdentifier') {
        newValue = newValue.replaceAll(/[\W_]+/g, '.');
      }
      setPending(key)(value.target.id, newValue);
    },
    [setPending]
  );

  const setPendingStorage = useCallback(
    (key) => (value) => {
      setPending(key)('storage_type', value);
    },
    [setPending]
  );

  const setPendingURIOption = useCallback(
    (key) => (value) => {
      if (value === 'srv') {
        setPending(key)('uri_option', value, 'port');
      } else {
        setPending(key)('uri_option', value);
      }
    },
    [setPending]
  );

  const setPendingPort = useCallback(
    (key) => (value) => {
      setPending(key)('port', value);
    },
    [setPending]
  );

  const setPendingIsActive = useCallback(
    (key) => (value) => {
      setPending(key)('isActive', value);
    },
    [setPending]
  );

  const addStorage = useCallback(() => {
    const timeStamp = new Date().getTime();
    setPending(timeStamp)('isManuallyAdded', true);
  }, [setPending]);

  const consolidatedStorages = useMemo(() => {
    const addedStorages = _.pickBy(
      pendingChanges,
      (storage) => storage.isManuallyAdded
    );
    if (!_.isEmpty(addedStorages)) {
      return { ...addedStorages, ...storageCredentials };
    }
    return storageCredentials;
  }, [storageCredentials, pendingChanges]);

  const postCombinedStorages = useCallback(
    (storageIdentifier) => (action) => (newStorageCredentials) => {
      const storageId =
        newStorageCredentials?.storageIdentifier ?? storageIdentifier;
      let newStorages;
      if (action === 'update') {
        newStorages = {
          ...storageCredentials,
          [storageId]: {
            ...newStorageCredentials,
            user_edited_at: new Date().toISOString(),
          },
        };
      }
      if (action === 'delete') {
        newStorages = _.omit(storageCredentials, storageId);
      }
      postStorageCredentials(newStorages);
    },
    [postStorageCredentials, storageCredentials]
  );

  const openNotification = useCallback((status) => {
    if (status === 'success') {
      notification.success({
        message: `Successfully updated Storages`,
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
        add={addStorage}
        isLoading={isLoading}
        error={variablesError}
        fetch={fetchStorageCredentials}
      />
      {_.isEmpty(consolidatedStorages) ? (
        <NoData
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          description="No Storages"
        />
      ) : (
        _.map(consolidatedStorages, (values, storageIdentifier) => (
          <ErrorBoundary domain="storage info" key={storageIdentifier}>
            <Storage
              values={values}
              isLoading={isLoading}
              pendingChanges={_.get(pendingChanges, storageIdentifier)}
              setPendingInput={setPendingInput}
              setPendingStorage={setPendingStorage}
              setPendingURIOption={setPendingURIOption}
              setPendingPort={setPendingPort}
              storageIdentifier={storageIdentifier}
              postStorageCredentials={postCombinedStorages(storageIdentifier)}
              toggleIsActive={setPendingIsActive(storageIdentifier)}
            />
          </ErrorBoundary>
        ))
      )}
    </Wrapper>
  );
};

export default Storages;
