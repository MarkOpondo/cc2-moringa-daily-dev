export function timeAgo(isoDate) {
  const seconds = Math.floor((Date.now() - new Date(isoDate).getTime()) / 1000);
  const units = [
    ["y", 31536000],
    ["mo", 2592000],
    ["d", 86400],
    ["h", 3600],
    ["m", 60],
  ];
  for (const [label, secs] of units) {
    const value = Math.floor(seconds / secs);
    if (value >= 1) return `${value}${label} ago`;
  }
  return "just now";
}

export function roleLabel(role) {
  switch (role) {
    case "admin":
      return "Admin";
    case "tech_writer":
      return "Tech Writer";
    default:
      return "Member";
  }
}

export function roleColorClass(role) {
  switch (role) {
    case "admin":
      return "text-role-admin";
    case "tech_writer":
      return "text-role-writer";
    default:
      return "text-role-user";
  }
}

export function initials(username = "") {
  return username.slice(0, 2).toUpperCase();
}
