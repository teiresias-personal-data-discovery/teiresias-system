import { useCallback, useRef, useEffect } from 'react';
import { Form, Input, Button } from 'antd';
import _ from 'lodash';
import styled from 'styled-components';
import Reward from 'react-rewards';

import Card from './Card';
import Flex from './Flex';

export const Error = styled.span`
  font-size: 15px;
  background: lightgrey;
  color: red;
`;

const messages = (error) => {
  if (error) {
    switch (error) {
      case 400:
        return 'Invalid login.';
      default:
        return 'Service unavailable.';
    }
  }
};

const defaultRules = {
  userName: [{ required: true, message: 'Username is mandatory' }],
  pwd: [{ required: true, message: 'Password is mandatory' }],
};

const Login = ({ title, isLoading, login, userError, wasSuccessful }) => {
  const buttonRef = useRef(null);

  const onFinish = useCallback(
    (credentials) => {
      login(credentials);
    },
    [login]
  );

  useEffect(() => {
    if (!isLoading && userError) {
      _.get(buttonRef, ['current', 'punishMe'], () => {})();
    }
  }, [userError, isLoading]);

  useEffect(() => {
    if (wasSuccessful) {
      _.get(buttonRef, ['current', 'rewardMe'], () => {})();
    }
  }, [wasSuccessful, isLoading]);

  return (
    <Card title={`${title} Login`} width="400px" dark>
      <Form name={`${_.camelCase(title)}_login`} onFinish={onFinish}>
        <Form.Item
          name={`${_.camelCase(title)}_userName`}
          rules={defaultRules.userName}
        >
          <Input
            id={`${_.camelCase(title)}_userName`}
            size="large"
            placeholder="User Name"
            allowClear
          />
        </Form.Item>
        <Form.Item name={`${_.camelCase(title)}_pwd`} rules={defaultRules.pwd}>
          <Input.Password
            id={`${_.camelCase(title)}_pwd`}
            size="large"
            placeholder="Password"
            allowClear
          />
        </Form.Item>
        <Flex space>
          <Error>{messages(userError)}</Error>
          <Reward type="emoji" ref={buttonRef}>
            <Button type="primary" loading={isLoading} htmlType="submit">
              Login
            </Button>
          </Reward>
        </Flex>
      </Form>
    </Card>
  );
};

export default Login;
