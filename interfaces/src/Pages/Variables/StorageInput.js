import { Input, InputNumber, Select } from 'antd';
import _ from 'lodash';

import styled from 'styled-components';

const StorageSelect = styled(Select)`
  width: 100%;
  height: 22px;
`;
const Port = styled(InputNumber)`
  width: 100%;
`;

const storageTypes = [
  { label: 'MongoDB', key: 'mongodb' },
  { label: 'PostgreSQL', key: 'postgres' },
];

export const storageOptions = [
  { label: 'mongodb://', key: 'mongodb', default: true },
  { label: 'mongodb+srv://', key: 'srv' },
];

export const InputFactory = ({
  valueKey,
  setPendingInput,
  setPendingStorage,
  setPendingURIOption,
  storageIdentifier,
  setPendingPort,
  value,
  isDisabled,
}) => {
  switch (valueKey) {
    case 'password':
      return (
        <Input.Password
          id={valueKey}
          size="small"
          value={value}
          onChange={setPendingInput(storageIdentifier)}
          disabled={isDisabled}
        />
      );
    case 'port':
      return (
        <Port
          id={valueKey}
          size="small"
          value={value}
          onChange={setPendingPort(storageIdentifier)}
          disabled={isDisabled}
        />
      );
    case 'storage_type':
      return (
        <StorageSelect
          value={value}
          onChange={setPendingStorage(storageIdentifier)}
          disabled={isDisabled}
        >
          {storageTypes.map(({ key, label }) => (
            <Select.Option key={key}>{label}</Select.Option>
          ))}
        </StorageSelect>
      );
    case 'uri_option':
      return (
        <StorageSelect
          value={value}
          onChange={setPendingURIOption(storageIdentifier)}
          disabled={isDisabled}
          defaultValue={_.chain(storageOptions)
            .find({ default: true })
            .get('label')
            .value()}
        >
          {storageOptions.map(({ key, label }) => (
            <Select.Option key={key}>{label}</Select.Option>
          ))}
        </StorageSelect>
      );
    default:
      return (
        <Input
          id={valueKey}
          size="small"
          value={value}
          onChange={setPendingInput(storageIdentifier)}
          disabled={isDisabled}
        />
      );
  }
};

export const InputEnrichedTitle = ({
  values,
  setPendingInput,
  pendingChanges,
  storageIdentifier,
}) =>
  values.isManuallyAdded ? (
    <Input
      placeholder="storage identifier"
      id="storageIdentifier"
      size="large"
      value={_.get(pendingChanges, 'storageIdentifier')}
      onChange={setPendingInput(storageIdentifier)}
    />
  ) : (
    <>{storageIdentifier}</>
  );
