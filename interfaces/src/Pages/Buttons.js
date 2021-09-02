import { Spin, Button } from 'antd';
import {
  SaveOutlined,
  PlusCircleOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import styled from 'styled-components';

import Flex from '../Base/Flex';

const Row = styled(Flex)`
  height: 50px;
`;

const Error = styled.h4`
  background: red;
  color: white;
  margin-bottom: 15px;
`;

const Buttons = ({ add, save, isLoading, error, fetch, children }) => (
  <Flex column align="center">
    {error && !isLoading && (
      <Flex>
        <Error>Error on loading data</Error>
      </Flex>
    )}
    <Row>
      <Flex space>
        <Flex>
          {fetch && (
            <Button
              size="large"
              icon={<ReloadOutlined />}
              onClick={fetch}
              loading={isLoading}
            >
              Refresh
            </Button>
          )}
          {add && !error && (
            <Button size="large" icon={<PlusCircleOutlined />} onClick={add}>
              New
            </Button>
          )}
        </Flex>
        <Flex end>
          {save && (
            <Button
              type="primary"
              size="large"
              icon={<SaveOutlined />}
              onClick={save}
              loading={isLoading}
            >
              Save
            </Button>
          )}
          {children && children}
        </Flex>
      </Flex>
      {isLoading && <Spin />}
    </Row>
  </Flex>
);

export default Buttons;
