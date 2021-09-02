import { useState, useCallback } from 'react';
import { Menu as AntdMenu, Layout } from 'antd';
import styled from 'styled-components';

import {
  SecurityScanOutlined,
  ScheduleOutlined,
  ClusterOutlined,
  CloudUploadOutlined,
  DeploymentUnitOutlined,
  BranchesOutlined,
} from '@ant-design/icons';
import _ from 'lodash';

import './App.css';
import { colors } from './Base/constants';
import Logo from './Base/Logo';
import Page from './Pages/Page';

const { Sider, Content: AntdContent } = Layout;

const Menu = styled(AntdMenu)`
  height: 100vh;
  width: 300px;
  background: ${colors.tertiary};
  > * {
    font-size: 1.3em;
  }
  .anticon {
    > * {
      height: 1.4em;
      width: 1.4em;
    }
  }
  .ant-menu-item-group-title {
    font-size: 1.3em;
    font-style: italic;
    color: ${colors.background};
  }
`;

const Side = styled(Sider)`
  height: 100%;
  min-height: 100vh;
  width: 300px !important;
  position: fixed;
  left: 0;
`;

const Group = styled(Menu.ItemGroup)`
  .ant-menu-item-group-title {
    cursor: default;
  }
`;

const Content = styled(AntdContent)`
  position: relative;
  overflow: initial;
  margin-left: 300px;
  min-height: 100vh;

  background: ${colors.background};
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background: rgba(32, 33, 36, 1);
`;

const content = {
  Inventory: [
    {
      key: 'reporting',
      label: 'Reports',
      icon: <SecurityScanOutlined />,
    },
  ],
  'Discovery Variables': [
    {
      key: 'git',
      label: 'Repositories',
      icon: <BranchesOutlined />,
    },
    {
      key: 'env',
      label: 'Storages',
      icon: <DeploymentUnitOutlined />,
    },
  ],
  'Discovery API': [
    {
      key: 'dataInput',
      label: 'Data Input',
      icon: <CloudUploadOutlined />,
    },
  ],
  'System Components': [
    {
      key: 'airflow',
      label: 'Scheduler',
      icon: <ScheduleOutlined />,
    },
    {
      key: 'flower',
      label: 'Monitoring',
      icon: <ClusterOutlined />,
    },
  ],
};

const App = ({ menu = content }) => {
  const [activeKey, setActiveKey] = useState('reporting');

  const changeMenuKey = useCallback(
    (event) => {
      switch (event.key) {
        case 'airflow':
          window.open(
            `${
              process.env.REACT_APP_AIRFLOW_BASE ||
              'https://airflow.docker.localhost'
            }`,
            '_blank'
          );
          break;
        case 'flower':
          window.open(
            `${
              process.env.REACT_APP_FLOWER_BASE ||
              'https://flower.docker.localhost'
            }`,
            '_blank'
          );
          break;
        default:
          setActiveKey(_.chain(event).get('keyPath').head().value());
      }
    },
    [setActiveKey]
  );

  return (
    <Layout>
      <Side>
        <Menu
          theme="dark"
          onClick={changeMenuKey}
          selectedKeys={activeKey}
          mode="inline"
        >
          <Logo />
          {_.map(menu, (group, key) => (
            <Group key={key} title={key}>
              {group.map(({ key, label, icon }) => (
                <Menu.Item key={key} icon={icon}>
                  {label}
                </Menu.Item>
              ))}
            </Group>
          ))}
        </Menu>
      </Side>
      <Content>
        <Page activeKey={activeKey} />
      </Content>
    </Layout>
  );
};

export default App;
