import React, { useEffect, useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import ItemCard from './ItemCard';
import api from '../../api';

function ItemList() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    api.getItems().then(response => {
      setItems(response.data);
    }).catch(error => {
      console.error('Error fetching items:', error);
    });
  }, []);

  return (
    <Container>
      <Row>
        {items.map(item => (
          <Col key={item.id} md={4}>
            <ItemCard item={item} />
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default ItemList;
