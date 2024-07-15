import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Connexion } from "./screens/Connexion";
import { Dashboard } from "./screens/Dashboard";
import { DashboardScreen } from "./screens/DashboardScreen";
import { DivWrapper } from "./screens/DivWrapper";
import { Screen4 } from "./screens/Screen4";
import { Screen5 } from "./screens/Screen5";
import { Screen6 } from "./screens/Screen6";
import { Screen7 } from "./screens/Screen7";
import { DashboardWrapper } from "./screens/DashboardWrapper";
import { DashboardClient } from "./screens/DashboardClient/DashboardClient";

const router = createBrowserRouter([
  {
    path: "/*",
    element: <Connexion />,
  },
  {
    path: "/connexion",
    element: <Connexion />,
  },
  {
    path: "/dashboard-1",
    element: <Dashboard />,
  },
  {
    path: "/dashboard-2",
    element: <DashboardScreen />,
  },
  {
    path: "/dashboard-4",
    element: <DivWrapper />,
  },
  {
    path: "/dashboard-5",
    element: <Screen4 />,
  },
  {
    path: "/dashboard-6",
    element: <Screen5 />,
  },
  {
    path: "/dashboard-9",
    element: <Screen6 />,
  },
  {
    path: "/dashboard-10",
    element: <Screen7 />,
  },
  {
    path: "/dashboard-3",
    element: <DashboardWrapper />,
  },
  {
    path: "/dashClient",
    element: <DashboardClient />,
  },
]);

export const App = () => {
  return <RouterProvider router={router} />;
};
