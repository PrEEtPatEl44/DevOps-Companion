import NextAuth from "next-auth";
import AzureADProvider from "next-auth/providers/azure-ad";
import { toast } from "sonner";
const { AZURE_AD_CLIENT_ID, AZURE_AD_CLIENT_SECRET, AZURE_AD_TENANT_ID } =
  process.env;
if (!AZURE_AD_CLIENT_ID || !AZURE_AD_CLIENT_SECRET || !AZURE_AD_TENANT_ID) {
  throw new Error("The Azure AD environment variables are not set.");
}
const handler = NextAuth({
    
    secret: process.env.NEXTAUTH_SECRET,
  providers: [
    AzureADProvider({
      clientId: AZURE_AD_CLIENT_ID,
      clientSecret: AZURE_AD_CLIENT_SECRET,
      tenantId: AZURE_AD_TENANT_ID,
    }),
  ],
  callbacks: {
    async jwt({ token, account }) {
      if (account) {
        token = Object.assign({}, token, {
          access_token: account.access_token,
        });
      }
      return token;
    },
    async session({ session, token }) {
      if (session) {
        session = Object.assign({}, session, {
          access_token: token.access_token,
        });
      }
      const response = await fetch('http://127.0.0.1:5000/api/receive-token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(session),  // Send the entire session object
      });

      const data = await response.json();
      if (response.ok) {
        toast.success('Token successfully sent to Flask API', { description: data.message });
      } else {
        toast.error('Failed to send token to Flask API', { description: data.message });
      }

      return session;
    },
  },
});


export { handler as GET, handler as POST };