import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

function Footer() {
  return (
    <footer className="bg-light text-center text-lg-start">
      <Container className="p-4">
        <Row>
          <Col lg={6} md={12} className="mb-4 mb-md-0">
            <h5 className="text-uppercase">Rosee Thrifts</h5>
            <p>
              Your go-to online thrift store for second-hand clothing items.
            </p>
          </Col>
          <Col lg={3} md={6} className="mb-4 mb-md-0">
            <h5 className="text-uppercase">Links</h5>
            <ul className="list-unstyled mb-0">
              <li><a href="#!" className="text-dark">Home</a></li>
              <li><a href="#!" className="text-dark">Shop</a></li>
              <li><a href="#!" className="text-dark">Cart</a></li>
            </ul>
          </Col>
          <Col lg={3} md={6} className="mb-4 mb-md-0">
            <h5 className="text-uppercase">Contact</h5>
            <ul className="list-unstyled mb-0">
              <li><a href="#!" className="text-dark">Email</a></li>
              <li><a href="#!" className="text-dark">Phone</a></li>
              <li><a href="#!" className="text-dark">Address</a></li>
            </ul>
          </Col>
        </Row>
      </Container>
      <div className="text-center p-3" style={{ backgroundColor: 'rgba(0, 0, 0, 0.2)' }}>
        © 2023 Rosee Thrifts
      </div>
    </footer>
  );
}

export default Footer;
