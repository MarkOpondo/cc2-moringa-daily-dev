import { useEffect, useState } from "react";
import { Ban, Check, CheckCircle2, FileWarning, Flag, Users, X } from "lucide-react";

import { listPendingContent, listReports, listUsers, resolveReport, toggleUserActive, updateContentStatus } from "../services/adminApi";
import { roleColorClass, roleLabel, timeAgo } from "../utils/format";
import EmptyState from "../components/ui/EmptyState";

const TABS = [
  { id: "queue", label: "Content queue", icon: FileWarning },
  { id: "users", label: "Users", icon: Users },
  { id: "reports", label: "Reports", icon: Flag },
];

export default function AdminDashboard() {
  const [tab, setTab] = useState("queue");
  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs font-mono text-sky-400 mb-1">// admin</p>
        <h1 className="text-2xl font-bold text-cream">Admin dashboard</h1>
      </div>
      <div className="flex gap-1 border-b border-navy-border">
        {TABS.map(({ id, label, icon: Icon }) => (
          <button key={id} onClick={() => setTab(id)} className={`flex items-center gap-1.5 px-4 py-2.5 text-sm border-b-2 -mb-px transition ${tab === id ? "border-sky-400 text-sky-400" : "border-transparent text-slate-400 hover:text-slate-300"}`}>
            <Icon className="w-3.5 h-3.5" /> {label}
          </button>
        ))}
      </div>
      {tab === "queue" && <ContentQueueTab />}
      {tab === "users" && <UsersTab />}
      {tab === "reports" && <ReportsTab />}
    </div>
  );
}

function ContentQueueTab() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  async function load() {
    try {
      setItems(await listPendingContent());
      setError("");
    } catch (requestError) {
      setError(requestError.message || "Unable to load the content queue.");
    }
  }

  useEffect(() => { load(); }, []);

  async function update(id, action) {
    try {
      await action(id);
      await load();
    } catch (requestError) {
      setError(requestError.message || "Unable to update content.");
    }
  }

  if (error) return <p className="text-red-400 text-sm">{error}</p>;
  if (items.length === 0) return <EmptyState icon={CheckCircle2} title="Queue is clear" description="No content is waiting on review right now." />;

  return (
    <div className="space-y-3">
      {items.map((item) => (
        <div key={item.id} className="p-4 rounded-xl border border-navy-border bg-navy">
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[11px] font-mono uppercase text-slate-400">{item.categories?.[0]?.name}</span>
                <span className="text-[10px] font-mono uppercase rounded px-1.5 py-0.5 border text-amber-400 border-amber-500/30">{item.status}</span>
              </div>
              <h3 className="font-display font-semibold text-cream">{item.title}</h3>
              <p className="text-xs text-slate-400 mt-1">by {item.author?.username} · {timeAgo(item.createdAt)}</p>
            </div>
            <div className="flex gap-2 shrink-0">
              <button onClick={() => update(item.id, (id) => updateContentStatus(id, "published"))} className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20"><Check className="w-3.5 h-3.5" /> Approve</button>
              <button onClick={() => update(item.id, (id) => updateContentStatus(id, "archived"))} className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20"><X className="w-3.5 h-3.5" /> Archive</button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function UsersTab() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  async function load() {
    try {
      setUsers(await listUsers());
      setError("");
    } catch (requestError) {
      setError(requestError.message || "Unable to load users.");
    }
  }

  useEffect(() => { load(); }, []);

  async function handleToggle(id) {
    try {
      await toggleUserActive(id);
      await load();
    } catch (requestError) {
      setError(requestError.message || "Unable to update user status.");
    }
  }

  if (error) return <p className="text-red-400 text-sm">{error}</p>;
  return (
    <div className="border border-navy-border rounded-xl overflow-hidden">
      <table className="w-full text-sm">
        <thead className="bg-navy-raised/95 text-slate-400 text-[11px] uppercase font-mono"><tr><th className="text-left px-4 py-2.5 font-medium">Username</th><th className="text-left px-4 py-2.5 font-medium">Role</th><th className="text-left px-4 py-2.5 font-medium">Status</th><th className="text-right px-4 py-2.5 font-medium">Action</th></tr></thead>
        <tbody className="divide-y divide-navy-border">
          {users.map((user) => (
            <tr key={user.id}>
              <td className="px-4 py-3 text-cream">{user.username}</td>
              <td className={`px-4 py-3 font-mono text-xs ${roleColorClass(user.role)}`}>{roleLabel(user.role)}</td>
              <td className="px-4 py-3"><span className={`text-xs font-mono ${user.isActive ? "text-emerald-400" : "text-slate-400"}`}>{user.isActive ? "Active" : "Deactivated"}</span></td>
              <td className="px-4 py-3 text-right"><button onClick={() => handleToggle(user.id)} className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-medium border transition ${user.isActive ? "border-red-500/30 text-red-400 hover:bg-red-500/10" : "border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10"}`}><Ban className="w-3 h-3" /> {user.isActive ? "Deactivate" : "Reactivate"}</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ReportsTab() {
  const [reports, setReports] = useState([]);
  const [error, setError] = useState("");

  async function load() {
    try {
      setReports(await listReports());
      setError("");
    } catch (requestError) {
      setError(requestError.message || "Unable to load reports.");
    }
  }

  useEffect(() => { load(); }, []);

  async function handleResolve(id) {
    try {
      await resolveReport(id);
      await load();
    } catch (requestError) {
      setError(requestError.message || "Unable to resolve report.");
    }
  }

  if (error) return <p className="text-red-400 text-sm">{error}</p>;
  if (reports.length === 0) return <EmptyState icon={Flag} title="No reports" description="Content flagged by the community will show up here." />;
  return (
    <div className="space-y-3">
      {reports.map((report) => (
        <div key={report.id} className="p-4 rounded-xl border border-navy-border bg-navy">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-sm text-cream">{report.content?.title || `Content #${report.contentId}`}</p>
              <p className="text-xs text-slate-400 mt-1">Reported by {report.reporter?.username} · {timeAgo(report.createdAt)}</p>
              <p className="text-xs text-slate-400 mt-2 italic">"{report.reason}"</p>
            </div>
            {report.status === "pending" ? <button onClick={() => handleResolve(report.id)} className="shrink-0 px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20">Mark resolved</button> : <span className="text-[11px] font-mono text-slate-400 shrink-0">Resolved</span>}
          </div>
        </div>
      ))}
    </div>
  );
}
