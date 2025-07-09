import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import productRoutes from './routes/productRoutes';
import userRoutes from './routes/userRoutes';
import orderRoutes from './routes/orderRoutes';

dotenv.config();

const app = express();
const port = process.env.PORT || 5002;

// ✅ Updated CORS configuration
const allowedOrigins = [
  'http://localhost:5173',
  'http://localhost:5174',
  'http://localhost:5175',
  'http://localhost:5176',
  'https://eco-ai-asst.netlify.app'
];

app.use(cors({
  origin: function (origin, callback) {
    // Allow requests with no origin (like curl, mobile apps, or server-side)
    if (!origin) return callback(null, true);

    if (allowedOrigins.includes(origin)) {
      return callback(null, true);
    } else {
      return callback(new Error('CORS policy: Not allowed by CORS'), false);
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// ✅ Handle preflight OPTIONS requests for all routes
app.options('*', cors());

// ✅ Middleware to parse JSON bodies
app.use(express.json());

// ✅ Routes
app.use('/products', productRoutes);
app.use('/users', userRoutes);
app.use('/orders', orderRoutes);

// ✅ Test route
app.get('/', (req, res) => {
  res.send('Server is running!');
});

// ✅ Error handling middleware
app.use((
  err: any,
  req: express.Request,
  res: express.Response,
  next: express.NextFunction
) => {
  console.error(err.stack);
  res.status(500).json({ message: err.message || 'Something went wrong!' });
});

// ✅ Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
