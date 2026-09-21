import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import logo from "../assets/logo.png";

const NAV_ITEMS = [
  { to: "/", label: "Home", icon: "◎", end: true },
  { to: "/assessment", label: "Assessment", icon: "🧭" },
  { to: "/mentor", label: "Mentor", icon: "💬" },
  { to: "/dashboard", label: "Dashboard", icon: "📊" },
  { to: "/history", label: "History", icon: "🕘" },
  { to: "/conversations", label: "Conversations", icon: "🗂" },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="side-brand">
          <img src={logo} alt="Brotherly" className="side-logo" />
          <span>Brotherly</span>
        </div>
        <nav className="side-nav">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => (isActive ? "active" : "")}
            >
              <span className="side-nav-icon">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        {user && (
          <div className="side-user">
            <div className="side-user-name" title={user.email}>
              {user.name}
            </div>
            <button className="side-logout" onClick={handleLogout}>
              Log out
            </button>
          </div>
        )}
      </aside>
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
