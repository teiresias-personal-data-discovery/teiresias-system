import { Component } from 'react';
import styled from 'styled-components';

const Message = styled.h2`
  color: #fff;
`;

class ErrorBoundary extends Component {
  state = { hasError: false };

  componentDidCatch(error, info) {
    this.setState({ hasError: true });
  }

  render() {
    if (this.state.hasError) {
      return (
        <Message>
          Something went wrong with this {this.props.domain ?? 'item'}.
        </Message>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
