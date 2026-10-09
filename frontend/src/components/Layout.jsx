import { useEffect, useState } from "react";
import { NavLink, useNavigate, Link } from "react-router-dom";
import {
  LayoutDashboard, Briefcase, CalendarClock, FileCheck2, AlertTriangle, Bell, LogOut,
  GraduationCap, UserCircle, Users, ShieldCheck, Sun, Moon,
} from "lucide-react";
import api from "../api";
import { logout, getRole, HOME } from "../auth";
import { applyTheme, getTheme } from "../theme";

const PROFILE = ["/profile", "My Profile", UserCircle];
const NAV = {
  student: [["/student", "My Readiness", GraduationCap], PROFILE],
  recruiter: [["/recruiter", "Jobs & Matches", Briefcase], PROFILE],
  officer: [
    ["/officer", "Dashboard", LayoutDashboard],
    ["/officer/students", "Students", Users],
    ["/officer/accounts", "Accounts", ShieldCheck],
    ["/recruiter", "Jobs & Matches", Briefcase],
    ["/officer/drives", "Drives", CalendarClock],
    ["/officer/offers", "Offers", FileCheck2],
    ["/officer/at-risk", "At-Risk Students", AlertTriangle],
    PROFILE,
  ],
  mentor: [["/officer", "Dashboard", LayoutDashboard], ["/officer/at-risk", "At-Risk Students", AlertTriangle], PROFILE],
};
const ROLE_LABEL = { student: "Student", recruiter: "Recruiter", officer: "Placement Officer", mentor: "Mentor" };
const WORKSPACE = {
  student: "Student Career Portal", recruiter: "Recruiter Workspace",
  officer: "Placement Operations", mentor: "Mentor Workspace",
};

export default function Layout({ children }) {
  const navigate = useNavigate();
  const [role, setRole] = useState(getRole());
  const [name, setName] = useState(localStorage.getItem("name") || "");
  const [notes, setNotes] = useState([]);
  const [open, setOpen] = useState(false);
  const [theme, setTheme] = useState(getTheme());

  useEffect(() => {
    api.get("/auth/me/").then(({ data }) => {
      localStorage.setItem("role", data.role);
      localStorage.setItem("name", data.name);
      setName(data.name);
      if (data.role !== role) {
        setRole(data.role);
        navigate(HOME[data.role], { replace: true });
      }
    }).catch(() => {});
  }, [role, navigate]);

  const load = () => api.get("/auth/notifications/").then((r) => setNotes(r.data)).catch(() => {});
  useEffect(() => { load(); }, []);

  const unread = notes.filter((n) => !n.is_read).length;
  const read = async (id) => { await api.post(`/auth/notifications/${id}/read/`); load(); };
  const doLogout = async () => { await logout(); navigate("/"); };
  const toggleTheme = () => { const t = theme === "dark" ? "light" : "dark"; applyTheme(t); setTheme(t); };
  const initials = name.split(" ").map((w) => w[0]).join("").slice(0, 2).toUpperCase() || "U";
  const links = NAV[role] || NAV.student;

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-30 flex items-center justify-between border-b border-slate-200 bg-white px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand text-sm font-extrabold tracking-wider text-white shadow-sm">CL</span>
          <div>
            <span className="text-base font-extrabold tracking-tight text-navy sm:text-lg">CAMPUSLINK</span>
            <p className="hidden text-xs text-slate-500 md:block">Campus-to-Corporate Placement Platform</p>
          </div>
        </div>

        <div className="flex items-center gap-2 sm:gap-3">
          <button onClick={toggleTheme} title="Toggle theme"
            className="rounded-full bg-slate-100 p-2.5 text-slate-600 hover:bg-slate-200">
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          </button>

          <div className="relative">
            <button onClick={() => setOpen(!open)} className="relative rounded-full bg-slate-100 p-2.5 text-slate-600 hover:bg-slate-200">
              <Bell size={18} />
              {unread > 0 && (
                <span className="absolute -right-1 -top-1 rounded-full bg-rose-500 px-1.5 text-[10px] font-bold text-white">{unread}</span>
              )}
            </button>
            {open && (
              <div className="absolute right-0 mt-2 max-h-96 w-80 overflow-auto rounded-2xl bg-white p-2 shadow-xl ring-1 ring-slate-200">
                {notes.length === 0 && <p className="p-4 text-sm text-slate-400">No notifications yet.</p>}
                {notes.map((n) => (
                  <div key={n.id} onClick={() => read(n.id)}
                    className={`cursor-pointer rounded-xl p-3 text-sm hover:bg-slate-50 ${n.is_read ? "opacity-60" : ""}`}>
                    <p className="font-semibold text-navy">{n.title}</p>
                    <p className="text-xs text-slate-600">{n.message}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <Link to="/profile" className="flex items-center gap-2.5 border-l border-slate-200 pl-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-full bg-brand text-xs font-bold text-white">{initials}</span>
            <span className="hidden sm:block">
              <p className="text-sm font-semibold leading-tight text-navy">{name}</p>
              <p className="text-[11px] text-slate-500">{ROLE_LABEL[role]}</p>
            </span>
          </Link>
        </div>
      </header>

      <div className="flex flex-1">
        <aside className="sticky top-[61px] hidden h-[calc(100vh-61px)] w-60 shrink-0 flex-col bg-slate-900 text-slate-300 md:flex">
          <div className="border-b border-slate-800 px-5 py-4">
            <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Active Workspace</p>
            <p className="mt-1 flex items-center justify-between text-sm font-semibold text-white">
              {WORKSPACE[role]}
              <span className={`h-2 w-2 rounded-full ${role === "student" ? "bg-emerald-400" : "bg-indigo-400"}`} />
            </p>
          </div>
          <nav className="flex-1 space-y-1 overflow-auto px-3 py-4">
            {links.map(([to, label, Icon]) => (
              <NavLink key={to + label} to={to} end
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-lg px-3 py-2.5 text-xs font-medium transition-colors ${
                    isActive ? "bg-brand font-semibold text-white shadow-sm" : "hover:bg-slate-800 hover:text-white"}`}>
                <Icon size={16} /> {label}
              </NavLink>
            ))}
          </nav>
          <button onClick={doLogout}
            className="m-3 flex items-center gap-3 rounded-lg border border-slate-700 bg-slate-800 px-3 py-2.5 text-xs font-medium hover:bg-slate-700 hover:text-white">
            <LogOut size={16} /> Logout
          </button>
        </aside>

        <main className="min-w-0 flex-1 p-4 sm:p-6 lg:p-8">
          {/* mobile nav (sidebar is hidden below md) */}
          <nav className="mb-4 flex gap-2 overflow-x-auto md:hidden">
            {links.map(([to, label]) => (
              <NavLink key={to + label} to={to} end
                className={({ isActive }) =>
                  `shrink-0 rounded-full px-3 py-1.5 text-xs font-medium ${isActive ? "bg-brand text-white" : "bg-slate-100 text-slate-600"}`}>
                {label}
              </NavLink>
            ))}
            <button onClick={doLogout} className="shrink-0 rounded-full bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-600">Logout</button>
          </nav>
          {children}
        </main>
      </div>
    </div>
  );
}
