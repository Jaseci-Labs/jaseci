import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import useUserInfo from "./useUserInfo";

function useGuard({ roles }: { roles: string[] }) {
  const { data: user, refetch } = useUserInfo();
  const [granted, setGranted] = useState(false);

  useEffect(() => {
    if (
      process.env.NODE_ENV === "development" ||
      process.env.NODE_ENV === "production"
    ) {
      setGranted(true);
      return;
    }

    if (!user && !user?.is_activated) {
      setGranted(false);
      // router.push("/?redirected=true&reason=not_activated");
    }

    if (roles.includes("superuser")) {
      if (user?.is_superuser) {
        setGranted(true);
      } else {
        setGranted(false);
        // router.push("/?redirected=true&reason=not_superuser");
      }
    }
    console.log({ user, roles });
  }, [user, roles]);

  return { user, granted, recheck: refetch };
}

export default useGuard;
