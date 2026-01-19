# 🏗 Arquitectura completa de Graf de Dades – Admin & Suggestions

## 1️⃣ Roles

| Rol                            | Qué puede hacer                                         | OAuth scopes                      |
| ------------------------------ | ------------------------------------------------------- | --------------------------------- |
| **Usuario normal / sugeridor** | Proponer nodos o aristas; identidad verificada          | `read:user`, `user:email`         |
| **Contributor / Admin**        | Ver solicitudes, aceptar/rechazar, crear PR, auto-merge | `repo`, `read:user`, `user:email` |

---

## 2️⃣ Componentes del sistema

| Componente                        | Tecnología         | Función                                                                                   |
| --------------------------------- | ------------------ | ----------------------------------------------------------------------------------------- |
| **Frontend público**              | HTML + JS          | Formulario de sugerencias; GitHub OAuth para identidad                                    |
| **Frontend admin**                | HTML + JS          | Dashboard para contributors/admins; GitHub OAuth con permisos de repo; crea PRs           |
| **Backend mínimo**                | Google Apps Script | API para recibir, almacenar y actualizar solicitudes en Google Sheets; valida token y rol |
| **Almacenamiento de solicitudes** | Google Sheets      | Guarda sugerencias con: `id`, `github_login`, `github_id`, `email`, `payload`, `status`   |
| **GitHub API**                    | REST               | Validación de collaborator, commits, creación de PRs, auto-merge                          |
| **GitHub Pages**                  | HTML + JS          | Visualización de la red pública usando `encrypted_data.txt`                               |

---

## 3️⃣ Flujo de usuario normal (hacer sugerencias)

1. Usuario abre formulario de sugerencia (`/suggest.html`).
2. Se autentica con GitHub OAuth (scopes mínimos: `read:user`, `user:email`).
3. Apps Script recibe sugerencia y token, valida que sea un token válido.
4. La sugerencia se guarda en Google Sheets con `status = pending`.
5. Usuario ve confirmación de que su sugerencia fue enviada.

**Nota:** Usuarios normales **no pueden acceder a PR ni dashboard**, no se piden permisos de `repo`.

---

## 4️⃣ Flujo admin / contributor (aceptar/rechazar sugerencias)

1. Contributor abre `/admin.html`.
2. Se autentica con GitHub OAuth (scopes: `repo`, `read:user`, `user:email`).
3. Apps Script valida:

   * Token válido
   * Usuario es collaborator del repo (`GET /repos/:owner/:repo/collaborators/:username`)
4. Si es collaborator: se muestra dashboard con todas las solicitudes pendientes.
5. Admin puede:

   * **Aceptar:** se crea branch, se modifica `encrypted_data.txt`, commit, PR y auto-merge
   * **Rechazar:** se actualiza `status = rejected` en Google Sheets

**Nota:** La identidad del sugeridor se guarda en la Sheet (`github_login`, `email`) y aparece en el dashboard.

---

## 5️⃣ Seguridad y roles

* **No se necesita contraseña extra.**
* Validación de roles y permisos se hace mediante GitHub OAuth + collaborator check.
* Usuarios normales solo tienen scopes mínimos, nunca pueden modificar repo.
* Admins con `repo` scope son los únicos que pueden crear PRs y mergear.
* Apps Script solo expone endpoints para:

  * Guardar sugerencias (`pending`)
  * Listar sugerencias (solo si usuario es contributor)
  * Actualizar status (`accepted` / `rejected`)

---

## 6️⃣ Flujo de PR

```
Contributor acepta sugerencia
   ↓
Frontend/admin.js llama GitHub API
   ↓
Crear branch temporal
   ↓
Modificar encrypted_data.txt
   ↓
Commit + Push
   ↓
Crear PR
   ↓
Auto-merge
```

* Autor del commit y PR: **contributor que acepta**
* Datos de sugeridor se registran en la Sheet y en el PR description (audit trail)

---

## 7️⃣ Ventajas de esta arquitectura

* Permisos mínimos por tipo de usuario
* Separación clara entre sugeridor y admin
* Seguridad realista sin contraseñas extra ni `credentials.enc`
* Fácil de mantener usando Google Apps Script + GitHub OAuth
* Todo el flujo se integra con GitHub Pages y D3.js sin backend pesado

