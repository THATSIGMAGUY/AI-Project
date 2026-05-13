import { EntityType } from "./types";

/** Maps an EntityType to the CSS custom property holding its dot color. */
export const typeColorVar: Record<EntityType, string> = {
  [EntityType.Person]:        "var(--color-type-person)",
  [EntityType.Organization]:  "var(--color-type-organization)",
  [EntityType.Location]:      "var(--color-type-location)",
  [EntityType.Event]:         "var(--color-type-event)",
  [EntityType.Document]:      "var(--color-type-document)",
  [EntityType.Asset]:         "var(--color-type-asset)",
  [EntityType.Communication]: "var(--color-type-communication)",
  [EntityType.Transaction]:   "var(--color-type-transaction)",
};
