export interface ApiUser {
  email: string;
  first_name: string;
  last_name: string;
  is_superuser: boolean;
}

export function transformApiUser(data: ApiUser) {
  return {
    email: data.email,
    firstName: data.first_name,
    lastName: data.last_name,
    isAdmin: data.is_superuser,
  };
}
