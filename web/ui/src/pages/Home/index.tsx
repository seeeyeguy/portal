import { useLoaderData } from "react-router";

import endpoints from "routes/api/endpoints";
import type { User } from "state/types/services/sso";

export default function Home() {
  const loaderData = useLoaderData() as { user: User };
  if (loaderData.user) {
    return (
      <>
        <div>Hello, {loaderData.user.firstName}!</div>
        <a href={endpoints.SERVICE.SSO.LOGOUT}>Logout</a>
      </>
    );
  }
  return <div>:x: 404</div>;
}
