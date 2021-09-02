import { Button, Switch, Popconfirm } from 'antd';
import _ from 'lodash';
import { SaveOutlined, DeleteOutlined } from '@ant-design/icons';
import styled from 'styled-components';

import Flex from '../../Base/Flex';

const Info = styled(Flex)`
  margin: 0 10px 0 15px;
  color: #666;
`;

const Toggle = styled(Switch)`
  margin-top: 4px;
`;

const StorageFooter = ({
  source,
  dateString,
  consolidatedValues,
  isValueMissing,
  toggleIsActive,
  removeStorage,
  isValid,
  updateStorage,
  isLoading,
}) => (
  <Flex column>
    <Flex space>
      <Info start align="flex-start">
        {!source && dateString && `Manually added at ${dateString}`}
        {source && source}
        {source && dateString && `, edited at ${dateString}`}
      </Info>
      <Toggle
        size="small"
        checked={_.get(consolidatedValues, 'isActive', !isValueMissing)}
        onChange={toggleIsActive}
        disabled={isValueMissing}
      />
      <Popconfirm
        title="Are you sure to delete this storage?"
        onConfirm={removeStorage}
        onCancel={null}
        okText="Yes"
        cancelText="No"
      >
        <Button
          size="small"
          shape="round"
          type="link"
          icon={<DeleteOutlined />}
          danger
        />
      </Popconfirm>
    </Flex>
    {isValid && (
      <Flex end>
        <Button
          type="primary"
          size="large"
          icon={<SaveOutlined />}
          onClick={updateStorage}
          loading={isLoading}
        >
          Save Changes
        </Button>
      </Flex>
    )}
  </Flex>
);

export default StorageFooter;
