import React from 'react';
import { Card, Button } from 'react-bootstrap';

function ItemCard({ item }) {
  return (
    <Card>
      <Card.Img variant="top" src={item.image_url} />
      <Card.Body>
        <Card.Title>{item.name}</Card.Title>
        <Card.Text>
          {item.description}
          <br />
          <strong>${item.price}</strong>
        </Card.Text>
        <Button variant="primary">Add to Cart</Button>
      </Card.Body>
    </Card>
  );
}

export default ItemCard;
