import { useMemo, useCallback } from 'react';
import { Tooltip } from 'antd';
import _ from 'lodash';
import {
  WarningOutlined,
  ExclamationCircleOutlined,
  UserAddOutlined,
} from '@ant-design/icons';
import styled from 'styled-components';

import Flex from '../../Base/Flex';
import Card from '../../Base/Card';
import { colors } from '../../Base/constants';
import { InputEnrichedTitle, InputFactory } from './StorageInput';
import StorageFooter from './StorageFooter';

const Title = styled(Flex)`
  width: 80px;
  margin: 0 10px 0 15px;
`;

const DefaultWrapper = styled(Flex)`
  width: 170px;
`;
const ErrorIcon = styled(WarningOutlined)`
  font-size: 16px;
  color: ${colors.error};
`;
const MissingIcon = styled(ExclamationCircleOutlined)`
  font-size: 16px;
  color: ${colors.error};
`;
const UserEditedIcon = styled(UserAddOutlined)`
  font-size: 16px;
  color: ${colors.primary};
`;

const InputWrapper = styled(Flex)`
  > * {
    margin: 10px 0;
  }
`;

const connectError = (error) =>
  `There was an error with this storage in the last discovery run: ${error}`;

const missingValueError = `Please add the missing values to enable the personal data discovery on that storage`;

const userEditedInfo = `Values have been edited, thus won't be overwritten by future storage discovery.`;

const credentialKeys = [
  { label: 'Host*', key: 'host', mandatory: true },
  { label: 'DB Name*', key: 'db', mandatory: true },
  {
    label: 'Port',
    key: 'port',
    disabled: { key: 'uri_option', value: 'srv' },
  },
  { label: 'User*', key: 'user', mandatory: true },
  { label: 'Type*', key: 'storage_type', mandatory: true },
  {
    label: 'URI*',
    key: 'uri_option',
    required: { key: 'storage_type', value: 'mongodb' },
  },
  { label: 'Password*', key: 'password', mandatory: true },
];
const mandatoryKeys = _.chain(credentialKeys)
  .filter(({ mandatory }) => mandatory)
  .map(({ key }) => key)
  .value();

const Storage = ({
  values,
  isLoading,
  pendingChanges,
  setPendingInput,
  setPendingStorage,
  setPendingURIOption,
  setPendingPort,
  storageIdentifier,
  postStorageCredentials,
  toggleIsActive,
}) => {
  const consolidatedValues = useMemo(() => {
    return _.omitBy(
      { ...values, ...pendingChanges },
      (value) => value === '' || _.isNil(value)
    );
  }, [values, pendingChanges]);

  const isValueMissing = useMemo(() => {
    const hasMandatoryKeys = mandatoryKeys.every(
      (key) => key in consolidatedValues
    );
    const hasCustomIdentifier = consolidatedValues.isManuallyAdded
      ? !_.isEmpty(consolidatedValues.storageIdentifier)
      : true;
    if (hasMandatoryKeys && hasCustomIdentifier) {
      return false;
    }
    return true;
  }, [consolidatedValues]);

  const updateStorage = useCallback(() => {
    const storageCredentials = _.omit(consolidatedValues, [
      'isManuallyAdded',
      'identifier',
    ]);
    postStorageCredentials('update')(storageCredentials);
  }, [consolidatedValues, postStorageCredentials]);

  const removeStorage = useCallback(() => {
    postStorageCredentials('delete')();
  }, [postStorageCredentials]);

  const dateString = useMemo(() => {
    if (consolidatedValues.user_edited_at) {
      try {
        return new Date(consolidatedValues.user_edited_at).toLocaleDateString();
      } catch {
        return consolidatedValues.user_edited_at;
      }
    }
  }, [consolidatedValues]);

  const source = useMemo(() => {
    if (consolidatedValues.source_repository) {
      return `Discovered in Repository: ${consolidatedValues.source_repository}, File: ${consolidatedValues.source_file}`;
    }
  }, [consolidatedValues]);

  const isValid = useMemo(() => !_.isEmpty(pendingChanges) && !isValueMissing, [
    pendingChanges,
    isValueMissing,
  ]);

  return (
    <Card
      width="600px"
      title={
        <InputEnrichedTitle
          values={values}
          setPendingInput={setPendingInput}
          storageIdentifier={storageIdentifier}
        />
      }
      key={storageIdentifier}
      info={
        <>
          {values.last_run_error && (
            <Tooltip title={connectError(values.last_run_error)}>
              <ErrorIcon />
            </Tooltip>
          )}
          {isValueMissing && (
            <Tooltip title={missingValueError}>
              <MissingIcon />
            </Tooltip>
          )}
          {values.user_edited_at && !values.added_at && (
            <Tooltip title={userEditedInfo}>
              <UserEditedIcon />
            </Tooltip>
          )}
        </>
      }
    >
      <InputWrapper wrap space>
        {credentialKeys.map(({ key, label, required, disabled }) => {
          if (
            required &&
            _.get(consolidatedValues, required?.key) !== required?.value
          ) {
            return <></>;
          }
          const isDisabled =
            _.get(consolidatedValues, disabled?.key, null) === disabled?.value;
          return (
            <Flex key={`${storageIdentifier}/${key}`}>
              <Title align="center">{label}:</Title>
              <DefaultWrapper>
                <InputFactory
                  valueKey={key}
                  setPendingInput={setPendingInput}
                  setPendingStorage={setPendingStorage}
                  setPendingURIOption={setPendingURIOption}
                  storageIdentifier={storageIdentifier}
                  value={consolidatedValues[key]}
                  pendingChanges={pendingChanges}
                  setPendingPort={setPendingPort}
                  isDisabled={isDisabled}
                />
              </DefaultWrapper>
            </Flex>
          );
        })}
      </InputWrapper>
      <StorageFooter
        source={source}
        dateString={dateString}
        consolidatedValues={consolidatedValues}
        isValueMissing={isValueMissing}
        toggleIsActive={toggleIsActive}
        removeStorage={removeStorage}
        isValid={isValid}
        updateStorage={updateStorage}
        isLoading={isLoading}
      />
    </Card>
  );
};

export default Storage;
