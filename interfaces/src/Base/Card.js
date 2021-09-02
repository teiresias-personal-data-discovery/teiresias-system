import styled, { css } from 'styled-components';
import { Space } from 'antd';

import { colors } from './constants';
import Flex from './Flex';

const Title = styled.span`
  font-size: 20px;
  font-style: italic;
  padding: 0 5px;
`;

const Wrapper = styled(Flex)`
  width: 100%;
`;

const Background = styled(Flex)`
  min-width: 200px;
  background: ${colors.secondary};
  color: ${colors.tertiary};
  ${(props) =>
    props.width &&
    css`
      width: ${props.width};
    `};

  ${(props) =>
    props.dark &&
    css`
      background: ${colors.tertiary};
      color: ${colors.background};
    `};

  border-radius: 5px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.3);
  padding: 5px 10px 15px 10px;
  margin: 10px;
  > * {
    width: 100%;
  }
`;

const Card = ({ children, title, width, info, dark }) => (
  <Background width={width} dark={dark} end>
    <Space direction="vertical">
      <Wrapper space width={width}>
        {title && <Title>{title}</Title>} {info && <Title>{info}</Title>}
      </Wrapper>
      {children}
    </Space>
  </Background>
);

export default Card;
