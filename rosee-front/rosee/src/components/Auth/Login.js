import React from 'react';
import { Button, Container, Row, Col } from 'react-bootstrap';
import { login } from '../../api';

function Login({ match }) {
  const { provider } = match.params;

  const handleLogin = () => {
    login(provider).then(response => {
      window.location.href = response.data;
    }).catch(error => {
      console.error('Error logging in:', error);
    });
  };

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col md={6}>
          <h2>Login with {provider}</h2>
          <Button onClick={handleLogin}>Login</Button>
        </Col>
      </Row>
    </Container>
  );
}

export default Login;
