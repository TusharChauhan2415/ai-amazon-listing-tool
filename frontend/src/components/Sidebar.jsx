const menuItems = ['Generate Listing', 'Saved Listings', 'Keyword Research', 'Competitor Analysis']

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 p-6 hidden md:block">
      <h1 className="text-xl font-bold text-white mb-8">AI Listing SaaS</h1>
      <ul className="space-y-2">
        {menuItems.map((item, idx) => (
          <li
            key={item}
            className={`p-3 rounded-lg text-sm ${idx === 0 ? 'bg-indigo-600 text-white' : 'text-slate-300 hover:bg-slate-800'}`}
          >
            {item}
          </li>
        ))}
      </ul>
    </aside>
  )
}
