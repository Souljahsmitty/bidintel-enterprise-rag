import React from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();
  function signInLocal() {
    // LOCAL: pretend Cognito returned a token for tenant 'demo'.
    localStorage.setItem("id_token", "local-dev-token");
    localStorage.setItem("tenant_id", "demo");
    navigate("/dashboard");
    // PRODUCTION: window.location = COGNITO_HOSTED_UI_URL;  (see docs/aws_iam_simulation.md)
  }
  return <button onClick={signInLocal}>Sign in (local dev)</button>;
}
