import type { ReactNode } from 'react';
import { ChevronRight, CircleAlert, Info, X } from 'lucide-react';
import type { Toast } from './useStudio';

export function Card({
  title,
  subtitle,
  icon,
  actions,
  children,
  className = '',
  bodyClassName = '',
}: {
  title?: ReactNode;
  subtitle?: ReactNode;
  icon?: ReactNode;
  actions?: ReactNode;
  children: ReactNode;
  className?: string;
  bodyClassName?: string;
}) {
  return (
    <section className={`card ${className}`}>
      {title && (
        <header className="card-head">
          {icon}
          <div style={{ flex: 1, minWidth: 0 }}>
            <h3>{title}</h3>
            {subtitle && <div className="muted">{subtitle}</div>}
          </div>
          {actions}
        </header>
      )}
      <div className={`card-body ${bodyClassName}`}>{children}</div>
    </section>
  );
}

export function Toggle({
  label,
  hint,
  checked,
  onChange,
  disabled,
}: {
  label: string;
  hint?: string;
  checked: boolean;
  onChange: () => void;
  disabled?: boolean;
}) {
  return (
    <div className="toggle-row" style={disabled ? { opacity: 0.55 } : undefined}>
      <div>
        <div className="label">{label}</div>
        {hint && <div className="hint">{hint}</div>}
      </div>
      <button
        type="button"
        className={`switch ${checked ? 'on' : ''}`}
        onClick={disabled ? undefined : onChange}
        aria-pressed={checked}
        aria-label={label}
        disabled={disabled}
      />
    </div>
  );
}

export function ToastStack({ toasts, onDismiss }: { toasts: Toast[]; onDismiss: (id: number) => void }) {
  return (
    <div className="toast-stack" role="status" aria-live="polite">
      {toasts.map((toast) => (
        <div className="toast" key={toast.id}>
          <span style={{ color: toast.tone === 'error' ? 'var(--danger)' : toast.tone === 'warn' ? 'var(--warn)' : 'var(--accent)', marginTop: 1 }}>
            {toast.tone === 'error' || toast.tone === 'warn' ? <CircleAlert size={14} /> : <Info size={14} />}
          </span>
          <span style={{ flex: 1 }}>{toast.message}</span>
          <button className="icon-btn" style={{ border: 0, background: 'transparent', padding: 0, color: 'var(--muted)' }} onClick={() => onDismiss(toast.id)} aria-label="Fermer">
            <X size={13} />
          </button>
        </div>
      ))}
    </div>
  );
}

export function RowLink({ title, subtitle, right, onClick }: { title: string; subtitle?: string; right?: ReactNode; onClick?: () => void }) {
  return (
    <div className="row">
      <div className="grow">
        <div className="t">{title}</div>
        {subtitle && <div className="s">{subtitle}</div>}
      </div>
      {right}
      {onClick && <button className="btn small ghost" onClick={onClick}><ChevronRight size={13} /></button>}
    </div>
  );
}
