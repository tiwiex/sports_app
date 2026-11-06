import "./styles.css";

export const metadata = {
  title: "Academy attendance",
  description: "Staff session rosters and offline attendance capture.",
  robots: { index: false, follow: false },
  manifest: "/assets/sports_app/attendance/manifest.webmanifest",
};

export default function Layout({ children }) {
  return <html lang="en"><body>{children}</body></html>;
}
