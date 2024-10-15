import * as React from 'react';
import * as ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
// import './index.css';

// include pages here
import Root from "./routes/Root"

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
  },
  // {
  //   path: "/page",
  //   element: <Element />,
  // },
]);



ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} /> 
  </React.StrictMode>
);
