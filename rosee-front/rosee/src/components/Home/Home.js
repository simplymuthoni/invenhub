import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Button } from 'react-bootstrap';

function Home() {
  return (
    <Container className="mt-5">
      <Row>
        <Col>
        <h1>Welcome to Rosee Thrifts</h1>
        <p>Find the best second-hand clothing items here!</p>
        <Button as={Link} to="/items" variant="primary">Shop Now</Button>
        </Col>
      </Row>
    </Container>
  );
}

export default Home;
