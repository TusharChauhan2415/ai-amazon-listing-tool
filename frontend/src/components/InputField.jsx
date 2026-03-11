export default function InputField({ label, name, value, onChange, placeholder }) {
  return (
    <label className="block">
      <span className="text-sm text-slate-300">{label}</span>
      <input
        name={name}
        value={value || ''}
        onChange={onChange}
        placeholder={placeholder}
        className="mt-1 w-full rounded-lg bg-slate-900 border border-slate-700 px-3 py-2 text-white"
      />
    </label>
  )
}
