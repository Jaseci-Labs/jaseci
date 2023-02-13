import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import useUserInfo from "./useUserInfo";

function useGuard({ roles }: { roles: string[] }) {
  const { data: user, refetch } = useUserInfo();
  const router = useRouter();
  const [granted, setGranted] = useState(false);

  useEffect(() => {
    if (!user && !user?.is_activated) {
      setGranted(false);
      router.push("/?redirected=true&reason=not_activated");
    }

    if (roles.includes("superuser")) {
      if (user?.is_superuser) {
        setGranted(true);
      } else {
        setGranted(false);
        router.push("/?redirected=true&reason=not_superuser");
      }
    }
  }, [user, roles]);

  return { user, granted, recheck: refetch };
}

export default useGuard;
