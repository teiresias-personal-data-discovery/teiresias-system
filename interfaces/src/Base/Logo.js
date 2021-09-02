import styled from 'styled-components';
import { colors, naming } from './constants';
import Flex from './Flex';

const Wrapper = styled(Flex)`
  padding: 36px 7px 100px 16px;
`;

const Title = styled.h1`
  font-size: 55px;
  color: ${colors.secondary};
  margin: 0 8px 0 0;
  line-height: 0.8;

  ::-moz-selection {
    color: ${colors.secondary};
    background: transparent;
    text-shadow: none;
  }

  ::selection {
    color: ${colors.secondary};
    background: transparent;
    text-shadow: none;
  }
  cursor: default;
`;

const Laut = styled.h3`
  z-index: 3;
  font-size: 18px;
  color: ${colors.yellow};
  margin: 14px 8px;

  ::-moz-selection {
    color: ${colors.yellow};
    background: transparent;
    text-shadow: none;
  }

  ::selection {
    color: ${colors.yellow};
    background: transparent;
    text-shadow: none;
  }
  cursor: default;
`;

const Logo = () => (
  <Wrapper column>
    <Flex>
      <Title>{naming.greek}</Title>
    </Flex>
    <Laut>{naming.laut}</Laut>
  </Wrapper>
);

export default Logo;
