import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Image, Button } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import api from '../../api';

function ItemDetail() {
  const { id } = useParams();
  const [item, setItem] = useState(null);

  useEffect(() => {
    api.get(`/items/${id}`).then(response => {
      setItem(response.data);
    }).catch(error => {
      console.error('Error fetching item:', error);
    });
  }, [id]);

  if (!item) {
    return <div>Loading...</div>;
  }

  return (
    <Container>
      <Row>
        <Col md={6}>
          <Image src={item.image_url} fluid />
        </Col>
        <Col md={6}>
          <h2>{item.name}</h2>
          <p>{item.description}</p>
          <h4>${item.price}</h4>
          <Button variant="primary">Add to Cart</Button>
        </Col>
      </Row>
    </Container>
  );
}

export default ItemDetail;
