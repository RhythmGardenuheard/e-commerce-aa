import { getProducts, createProduct, updateProduct, deleteProduct } from '../actions/products';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('http://localhost:8000/api/products', (req, res, ctx) => {
    return res(ctx.json([{ id: 1, name: 'Product 1', price: 10.99, stock: 100 }]));
  }),
  rest.post('http://localhost:8000/api/products', (req, res, ctx) => {
    return res(ctx.json({ id: 1, name: 'New Product', price: 15.99, stock: 50 }));
  }),
  rest.put('http://localhost:8000/api/products/1', (req, res, ctx) => {
    return res(ctx.json({ id: 1, name: 'Updated Product', price: 20.99, stock: 75 }));
  }),
  rest.delete('http://localhost:8000/api/products/1', (req, res, ctx) => {
    return res(ctx.status(200));
  }),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Product Actions', () => {
  const token = 'fake_token';

  test('getProducts should return products', async () => {
    const result = await getProducts(token);
    expect(result).toHaveLength(1);
    expect(result[0].name).toBe('Product 1');
  });

  test('createProduct should return new product', async () => {
    const result = await createProduct({ name: 'New Product', price: 15.99, stock: 50 }, token);
    expect(result.name).toBe('New Product');
  });

  test('updateProduct should return updated product', async () => {
    const result = await updateProduct(1, { name: 'Updated Product', price: 20.99, stock: 75 }, token);
    expect(result.name).toBe('Updated Product');
  });

  test('deleteProduct should not throw', async () => {
    await expect(deleteProduct(1, token)).resolves.not.toThrow();
  });
});