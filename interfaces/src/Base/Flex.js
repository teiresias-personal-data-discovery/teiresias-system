import styled, { css } from "styled-components";

const Flex = styled.div`
  display: flex;
  flex-direction: ${(props) => (props.column ? "column" : "row")};
  flex: ${(props) => props.flex || "0 1 auto"};
  flex-wrap: initial;

  ${(props) =>
    props.width &&
    css`
      width: ${props.width};
    `};

  ${(props) =>
    props.wrap &&
    css`
      flex-wrap: wrap;
    `};

  ${(props) =>
    props.align &&
    css`
      align-items: ${props.align};
    `};

  ${(props) =>
    props.space &&
    css`
      justify-content: space-between;
    `};

  ${(props) =>
    props.center &&
    css`
      justify-content: center;
    `};

  ${(props) =>
    props.start &&
    css`
      justify-content: flex-start;
    `};

  ${(props) =>
    props.end &&
    css`
      justify-content: flex-end;
    `};

  justify-content: ${(props) => props.justify};
`;

export default Flex;
